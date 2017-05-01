from featurerequest import app, db
import sys 
if __name__ == "__main__":
    if "--setup" in sys.argv:
        with app.app_context():
            db.create_all()
            print("Database tables created.")
    if "--populate" in sys.argv:
        with app.app_context():
            from featurerequest.models import User, Client, ClientNote, Product,\
                                              Feature, FeatureTodo, FeatureNote
            # Users
            users = [
                User(username='admin', role='Administrator'),
                User(username='employee', role='Employee'),
                User(username='client', role='Client')
            ]
            for user in users:
                db.session.add(user)
            # Clients
            clients = [
                Client(name='Client A', poc='Steve', email='steve@clienta.com', phone='1234567890', user_id=1),
                Client(name='Client B', poc='Nicole', email='nicole@clientb.com', phone='1234567890', user_id=1),
                Client(name='Client C', poc='Jess', email='jess@clientc.com', phone='1234567890', user_id=1),
                ]
            for client in clients:
                db.session.add(client)
            # Client Notes
            c_notes = [
                ClientNote(user_id=1, client_id=1, note='May be willing to start a new project with us.'),
                ClientNote(user_id=1, client_id=2, note='May be willing to start a new project with us.'),
                ClientNote(user_id=1, client_id=3, note='May be willing to start a new project with us.')
            ]
            for note in c_notes:
                db.session.add(note)
            # Product Areas
            products = [
                Product(user_id=1, name='Policies', description=''),
                Product(user_id=1, name='Billing', description=''),
                Product(user_id=1, name='Claims', description=''),
                Product(user_id=1, name='Reports', description='')
            ]
            for product in products:
                db.session.add(product)
            # Features
            features = [
                Feature(user_id=1, client_id=1, product_id=1, title='Test Feature 1', description='', priority=1),
                Feature(user_id=1, client_id=1, product_id=2, title='Test Feature 2', description='', priority=2),
                Feature(user_id=1, client_id=1, product_id=3, title='Test Feature 3', description='', priority=3),
                Feature(user_id=1, client_id=2, product_id=1, title='Test Feature 1', description='', priority=1),
                Feature(user_id=1, client_id=2, product_id=2, title='Test Feature 2', description='', priority=2),
                Feature(user_id=1, client_id=3, product_id=4, title='Test Feature', description='', priority=1),
            ]
            for feature in features:
                db.session.add(feature)
            # Feature To-dos
            todos = [
                FeatureTodo(user_id=1, feature_id=1, priority=1, todo='Beam me up, Scotty'),
                FeatureTodo(user_id=1, feature_id=2, priority=1, todo='Beam me up, Scotty'),
                FeatureTodo(user_id=1, feature_id=3, priority=1, todo='Beam me up, Scotty'),
                FeatureTodo(user_id=1, feature_id=4, priority=1, todo='Beam me up, Scotty'),
                FeatureTodo(user_id=1, feature_id=5, priority=1, todo='Beam me up, Scotty'),
                FeatureTodo(user_id=1, feature_id=6, priority=1, todo='Beam me up, Scotty'),
                FeatureTodo(user_id=1, feature_id=6, priority=2, todo='Now beam me back!'),
            ]
            for todo in todos:
                db.session.add(todo)
            f_notes = [
                FeatureNote(user_id=1, feature_id=1, note='We may have to upgrade the MySQL instance RAM for this.'),
                FeatureNote(user_id=1, feature_id=2, note='We may have to upgrade the MySQL instance RAM for this.'),
                FeatureNote(user_id=1, feature_id=6, note='We may have to upgrade the MySQL instance RAM for this.'),
            ]
            for note in f_notes:
                db.session.add(note)
            db.session.commit()
            db.session.commit()
            print("Database populated with test data.")
    else:
        app.run(debug=True)