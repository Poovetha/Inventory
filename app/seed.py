from datetime import datetime, timedelta
from random import randint, choice
from . import db
from .models import Product, Location, ProductMovement


def run_seed():
    db.create_all()

    products_seed = [
        Product(name='Product A'),
        Product(name='Product B'),
        Product(name='Product C'),
        Product(name='Product D'),
    ]

    locations_seed = [
        Location(name='Location X'),
        Location(name='Location Y'),
        Location(name='Location Z'),
    ]

    if Product.query.count() == 0:
        db.session.add_all(products_seed)
    if Location.query.count() == 0:
        db.session.add_all(locations_seed)

    db.session.commit()

    products = Product.query.all()
    locations = Location.query.all()

    # Create some movements
    existing = {m.movement_id for m in ProductMovement.query.all()}
    base_time = datetime.utcnow() - timedelta(days=5)
    counter = 1

    def next_id():
        nonlocal counter
        mid = f"M{counter:03d}"
        counter += 1
        return mid

    if products and locations:
        # Inbounds to first location
        first_loc_id = locations[0].location_id
        for _ in range(5):
            pid = choice(products).product_id
            mid = next_id()
            if mid in existing:
                continue
            mv = ProductMovement(
                movement_id=mid,
                timestamp=base_time + timedelta(hours=counter),
                product_id=pid,
                from_location=None,
                to_location=first_loc_id,
                qty=randint(5, 15),
            )
            db.session.add(mv)

        # Transfers and outbounds
        for _ in range(15):
            pid = choice(products).product_id
            action = randint(0, 2)
            mid = next_id()
            if mid in existing:
                continue
            if action == 0:
                # inbound to random
                to_loc = choice(locations).location_id
                mv = ProductMovement(
                    movement_id=mid,
                    timestamp=base_time + timedelta(hours=counter),
                    product_id=pid,
                    from_location=None,
                    to_location=to_loc,
                    qty=randint(1, 10),
                )
            elif action == 1:
                # outbound from random
                from_loc = choice(locations).location_id
                mv = ProductMovement(
                    movement_id=mid,
                    timestamp=base_time + timedelta(hours=counter),
                    product_id=pid,
                    from_location=from_loc,
                    to_location=None,
                    qty=randint(1, 8),
                )
            else:
                # transfer
                from_loc = choice(locations).location_id
                to_loc = choice([l.location_id for l in locations if l.location_id != from_loc])
                mv = ProductMovement(
                    movement_id=mid,
                    timestamp=base_time + timedelta(hours=counter),
                    product_id=pid,
                    from_location=from_loc,
                    to_location=to_loc,
                    qty=randint(1, 6),
                )
            db.session.add(mv)

        db.session.commit()
        print('Seed completed')
