from flask import Blueprint, render_template, redirect, url_for, request, flash
from sqlalchemy import func, case
from . import db
from .models import Product, Location, ProductMovement
from .forms import ProductForm, LocationForm, MovementForm

main_bp = Blueprint('main', __name__)


@main_bp.route('/')
def index():
    return render_template('index.html')


# Products
@main_bp.route('/products')
def products_list():
    products = Product.query.order_by(Product.product_id).all()
    return render_template('products/list.html', products=products)


@main_bp.route('/products/add', methods=['GET', 'POST'])
def products_add():
    form = ProductForm()
    if form.validate_on_submit():
        product = Product(
            name=form.name.data.strip(),
            description=form.description.data.strip() if form.description.data else None,
        )
        db.session.add(product)
        db.session.commit()
        flash('Product created', 'success')
        return redirect(url_for('main.products_list'))
    return render_template('products/form.html', form=form, is_edit=False)


@main_bp.route('/products/<int:product_id>/edit', methods=['GET', 'POST'])
def products_edit(product_id):
    product = Product.query.get_or_404(product_id)
    form = ProductForm(obj=product)
    if form.validate_on_submit():
        product.name = form.name.data.strip()
        product.description = form.description.data.strip() if form.description.data else None
        db.session.commit()
        flash('Product updated', 'success')
        return redirect(url_for('main.products_list'))
    return render_template('products/form.html', form=form, is_edit=True)


@main_bp.post('/products/<int:product_id>/delete')
def products_delete(product_id):
    product = Product.query.get_or_404(product_id)
    db.session.delete(product)
    db.session.commit()
    flash('Product deleted', 'info')
    return redirect(url_for('main.products_list'))


# Locations
@main_bp.route('/locations')
def locations_list():
    locations = Location.query.order_by(Location.location_id).all()
    return render_template('locations/list.html', locations=locations)


@main_bp.route('/locations/add', methods=['GET', 'POST'])
def locations_add():
    form = LocationForm()
    if form.validate_on_submit():
        location = Location(
            name=form.name.data.strip(),
            address=form.address.data.strip() if form.address.data else None,
        )
        db.session.add(location)
        db.session.commit()
        flash('Location created', 'success')
        return redirect(url_for('main.locations_list'))
    return render_template('locations/form.html', form=form, is_edit=False)


@main_bp.route('/locations/<int:location_id>/edit', methods=['GET', 'POST'])
def locations_edit(location_id):
    location = Location.query.get_or_404(location_id)
    form = LocationForm(obj=location)
    if form.validate_on_submit():
        location.name = form.name.data.strip()
        location.address = form.address.data.strip() if form.address.data else None
        db.session.commit()
        flash('Location updated', 'success')
        return redirect(url_for('main.locations_list'))
    return render_template('locations/form.html', form=form, is_edit=True)


@main_bp.post('/locations/<int:location_id>/delete')
def locations_delete(location_id):
    location = Location.query.get_or_404(location_id)
    db.session.delete(location)
    db.session.commit()
    flash('Location deleted', 'info')
    return redirect(url_for('main.locations_list'))


# Movements
@main_bp.route('/movements')
def movements_list():
    movements = (
        ProductMovement.query.order_by(ProductMovement.timestamp.desc()).all()
    )
    return render_template('movements/list.html', movements=movements)


def _choices_with_blank(items, value_attr, label_attr):
    choices = [('', '— None —')]
    for item in items:
        choices.append((getattr(item, value_attr), getattr(item, label_attr)))
    return choices


@main_bp.route('/movements/add', methods=['GET', 'POST'])
def movements_add():
    form = MovementForm()
    form.product_id.choices = [(str(p.product_id), f"{p.product_id} — {p.name}") for p in Product.query.order_by(Product.product_id)]
    locations = Location.query.order_by(Location.location_id)
    form.from_location.choices = _choices_with_blank(locations, 'location_id', 'name')
    form.to_location.choices = _choices_with_blank(locations, 'location_id', 'name')

    if form.validate_on_submit():
        from_loc = form.from_location.data or None
        to_loc = form.to_location.data or None
        if not from_loc and not to_loc:
            flash('Either From or To location must be provided', 'warning')
        elif from_loc and to_loc and from_loc == to_loc:
            flash('From and To cannot be the same', 'warning')
        else:
            mv = ProductMovement(
                movement_id=form.movement_id.data.strip(),
                product_id=int(form.product_id.data),
                from_location=int(from_loc) if from_loc else None,
                to_location=int(to_loc) if to_loc else None,
                qty=form.qty.data,
            )
            db.session.add(mv)
            db.session.commit()
            flash('Movement recorded', 'success')
            return redirect(url_for('main.movements_list'))

    return render_template('movements/form.html', form=form, is_edit=False)


@main_bp.route('/movements/<movement_id>/edit', methods=['GET', 'POST'])
def movements_edit(movement_id):
    mv = ProductMovement.query.get_or_404(movement_id)
    form = MovementForm(obj=mv)
    form.movement_id.render_kw = {'readonly': True}
    form.product_id.choices = [(str(p.product_id), f"{p.product_id} — {p.name}") for p in Product.query.order_by(Product.product_id)]
    locations = Location.query.order_by(Location.location_id)
    form.from_location.choices = _choices_with_blank(locations, 'location_id', 'name')
    form.to_location.choices = _choices_with_blank(locations, 'location_id', 'name')

    if form.validate_on_submit():
        from_loc = form.from_location.data or None
        to_loc = form.to_location.data or None
        if not from_loc and not to_loc:
            flash('Either From or To location must be provided', 'warning')
        elif from_loc and to_loc and from_loc == to_loc:
            flash('From and To cannot be the same', 'warning')
        else:
            mv.product_id = int(form.product_id.data)
            mv.from_location = int(from_loc) if from_loc else None
            mv.to_location = int(to_loc) if to_loc else None
            mv.qty = form.qty.data
            db.session.commit()
            flash('Movement updated', 'success')
            return redirect(url_for('main.movements_list'))

    return render_template('movements/form.html', form=form, is_edit=True)


@main_bp.post('/movements/<movement_id>/delete')
def movements_delete(movement_id):
    mv = ProductMovement.query.get_or_404(movement_id)
    db.session.delete(mv)
    db.session.commit()
    flash('Movement deleted', 'info')
    return redirect(url_for('main.movements_list'))


# Report
@main_bp.route('/report')
def report():
    agg = (
        db.session.query(
            Product.product_id.label('product_id'),
            Product.name.label('product_name'),
            Location.location_id.label('location_id'),
            Location.name.label('location_name'),
            func.coalesce(
                func.sum(
                    case(
                        (
                            (ProductMovement.to_location == Location.location_id),
                            ProductMovement.qty,
                        ),
                        else_=0,
                    )
                    - case(
                        (
                            (ProductMovement.from_location == Location.location_id),
                            ProductMovement.qty,
                        ),
                        else_=0,
                    )
                ),
                0,
            ).label('qty')
        )
        .select_from(ProductMovement)
        .join(Product, Product.product_id == ProductMovement.product_id)
        .outerjoin(Location, (
            (Location.location_id == ProductMovement.to_location)
            | (Location.location_id == ProductMovement.from_location)
        ))
        .group_by(Product.product_id, Product.name, Location.location_id, Location.name)
        .having(func.coalesce(func.sum(case((ProductMovement.to_location == Location.location_id, ProductMovement.qty), else_=0) - case((ProductMovement.from_location == Location.location_id, ProductMovement.qty), else_=0)), 0) != 0)
        .order_by(Product.product_id, Location.location_id)
        .all()
    )

    return render_template('report.html', rows=agg)
