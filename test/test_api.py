"""
Basic tests of the RESTful API. More comprehensive tests would include
checking the values retrieved against the dummy values entered on setup.
"""
import json
from test import MyTest
from featurerequest.models import Client

class UserTest(MyTest):
    base_url = '/user'
    def test_get(self):
        """ 
        GET: /user
        User Roles: Employee, Administrator
        """
        # Test getting all users
        response = self.client.get(self.base_url)
        assert response.status_code == 403
        user_response = dict(client=403, employee=200, admin=200)
        for user in user_response:
            self.client.get('/login_test/' + user)
            response = self.client.get(self.base_url)
            assert response.status_code == user_response[user]
        response = self.client.get('/logout')
        # Test for the retrieval of one user
        response = self.client.get(self.base_url + '/1')
        assert response.status_code == 403
        user_response = dict(client=403, employee=200, admin=200)
        for user in user_response:
            self.client.get('/login_test/' + user)
            response = self.client.get(self.base_url + '/1')
            #print('User:', user, 'Expected Response:', user_response[user], 'Actual Response:', response.status_code)
            assert response.status_code == user_response[user]
            if user_response[user] == 200:
                assert response.json['user']['id'] == 1
                assert response.json['user']['username'] == 'admin'
                assert response.json['user']['role'] == 'Administrator'

    def test_post(self):
        """ 
        POST: /user
        User Roles: Administrator
        """
        data = dict(username='new_user', role='Client')
        response = self.client.post(self.base_url, data=json.dumps(data), content_type='application/json')
        assert response.status_code == 403
        user_response = dict(client=403, employee=403, admin=201)
        for user in user_response:
            self.client.get('/login_test/' + user)
            response = self.client.post(self.base_url, data=json.dumps(data), content_type='application/json')
            #print('User:', user, 'Expected Response:', user_response[user], 'Actual Response:', response.status_code)
            assert response.status_code == user_response[user]


class ClientTest(MyTest):
    base_url = '/client'
    def test_get(self):
        """ 
        GET: /client
        User Roles: Employee, Administrator
        """
        # Test getting all clients
        response = self.client.get(self.base_url)
        assert response.status_code == 403
        user_response = dict(client=403, employee=200, admin=200)
        for user in user_response:
            self.client.get('/login_test/' + user)
            response = self.client.get(self.base_url)
            assert response.status_code == user_response[user]
        response = self.client.get('/logout')
        # Test for the retrieval of this client.
        response = self.client.get(self.base_url + '/1')
        assert response.status_code == 403
        user_response = dict(client=403, employee=200, admin=200)
        for user in user_response:
            self.client.get('/login_test/' + user)
            response = self.client.get(self.base_url + '/1')
            #print('User:', user, 'Expected Response:', user_response[user], 'Actual Response:', response.status_code)
            assert response.status_code == user_response[user]
            if user_response[user] == 200:
                assert response.json['client']['name'] == 'Client A'

    def test_post(self):
        """ 
        POST: /client
        User Roles: Administrator
        """
        data = dict(name='Test Client', email='admin@testclient.com', phone='1234567890')
        response = self.client.post(self.base_url, data=json.dumps(data), content_type='application/json')
        assert response.status_code == 403
        user_response = dict(client=403, employee=403, admin=201)
        for user in user_response:
            self.client.get('/login_test/' + user)
            response = self.client.post(self.base_url, data=json.dumps(data), content_type='application/json')
            assert response.status_code == user_response[user]


class ClientNoteTest(MyTest):
    base_url = '/clientnote'
    def test_get(self):
        """ 
        GET: /clientnote
        User Roles: Employee, Administrator
        """
        # Test getting all users
        response = self.client.get(self.base_url)
        assert response.status_code == 403
        user_response = dict(client=403, employee=200, admin=200)
        for user in user_response:
            self.client.get('/login_test/' + user)
            response = self.client.get(self.base_url)
            #print('User:', user, 'Expected Response:', user_response[user], 'Actual Response:', response.status_code)
            assert response.status_code == user_response[user]
        response = self.client.get('/logout')
        # Test for the retrieval of one user
        response = self.client.get(self.base_url + '/1')
        assert response.status_code == 403
        user_response = dict(client=403, employee=200, admin=200)
        for user in user_response:
            self.client.get('/login_test/' + user)
            response = self.client.get(self.base_url + '/1')
            #print('User:', user, 'Expected Response:', user_response[user], 'Actual Response:', response.status_code)
            assert response.status_code == user_response[user]

    def test_post(self):
        """ 
        POST: /clientnote
        User Roles: Employee, Administrator
        """
        data = dict(user_id=1, client_id=1, note='May be willing to start a new project with us.')
        response = self.client.post(self.base_url, data=json.dumps(data), content_type='application/json')
        assert response.status_code == 403
        user_response = dict(client=403, employee=201, admin=201)
        for user in user_response:
            self.client.get('/login_test/' + user)
            response = self.client.post(self.base_url, data=json.dumps(data), content_type='application/json')
            #print('User:', user, 'Expected Response:', user_response[user], 'Actual Response:', response.status_code)
            assert response.status_code == user_response[user]


class ProductTest(MyTest):
    base_url = '/product'
    def test_get(self):
        """ 
        GET: /product
        User Roles: Employee, Administrator
        """
        # Test getting all users
        response = self.client.get(self.base_url)
        assert response.status_code == 403
        user_response = dict(client=403, employee=200, admin=200)
        for user in user_response:
            self.client.get('/login_test/' + user)
            response = self.client.get(self.base_url)
            assert response.status_code == user_response[user]
        response = self.client.get('/logout')
        # Test for the retrieval of one user
        response = self.client.get(self.base_url + '/1')
        assert response.status_code == 403
        user_response = dict(client=403, employee=200, admin=200)
        for user in user_response:
            self.client.get('/login_test/' + user)
            response = self.client.get(self.base_url + '/1')
            #print('User:', user, 'Expected Response:', user_response[user], 'Actual Response:', response.status_code)
            assert response.status_code == user_response[user]

    def test_post(self):
        """ 
        POST: /product
        User Roles: Administrator
        """
        data = dict(user_id=1, name='Imaging')
        response = self.client.post(self.base_url, data=json.dumps(data), content_type='application/json')
        assert response.status_code == 403
        user_response = dict(client=403, employee=403, admin=201)
        for user in user_response:
            self.client.get('/login_test/' + user)
            response = self.client.post(self.base_url, data=json.dumps(data), content_type='application/json')
            #print('User:', user, 'Expected Response:', user_response[user], 'Actual Response:', response.status_code)
            assert response.status_code == user_response[user]


class FeatureTest(MyTest):
    base_url = '/feature'
    def test_get(self):
        """ 
        GET: /feature
        User Roles: Employee, Administrator
        """
        # Test getting all users
        response = self.client.get(self.base_url)
        assert response.status_code == 403
        user_response = dict(client=403, employee=200, admin=200)
        for user in user_response:
            self.client.get('/login_test/' + user)
            response = self.client.get(self.base_url)
            assert response.status_code == user_response[user]
        response = self.client.get('/logout')
        # Test for the retrieval of one user
        response = self.client.get(self.base_url + '/1')
        assert response.status_code == 403
        user_response = dict(client=403, employee=200, admin=200)
        for user in user_response:
            self.client.get('/login_test/' + user)
            response = self.client.get(self.base_url + '/1')
            #print('User:', user, 'Expected Response:', user_response[user], 'Actual Response:', response.status_code)
            assert response.status_code == user_response[user]

    def test_post(self):
        """ 
        POST: /feature
        User Roles: Employee, Administrator
        """
        data = dict(user_id=1, client_id=1, product_id=1, title='Test Feature 4', description='', priority=4)
        response = self.client.post(self.base_url, data=json.dumps(data), content_type='application/json')
        assert response.status_code == 403
        user_response = dict(client=403, employee=201, admin=201)
        for user in user_response:
            self.client.get('/login_test/' + user)
            response = self.client.post(self.base_url, data=json.dumps(data), content_type='application/json')
            #print('User:', user, 'Expected Response:', user_response[user], 'Actual Response:', response.status_code)
            assert response.status_code == user_response[user]


class FeatureTodoTest(MyTest):
    base_url = '/featuretodo'
    def test_get(self):
        """ 
        GET: /featuretodo
        User Roles: Employee, Administrator
        """
        # Test getting all users
        response = self.client.get(self.base_url)
        assert response.status_code == 403
        user_response = dict(client=403, employee=200, admin=200)
        for user in user_response:
            self.client.get('/login_test/' + user)
            response = self.client.get(self.base_url)
            assert response.status_code == user_response[user]
        response = self.client.get('/logout')
        # Test for the retrieval of one user
        response = self.client.get(self.base_url + '/1')
        assert response.status_code == 403
        user_response = dict(client=403, employee=200, admin=200)
        for user in user_response:
            self.client.get('/login_test/' + user)
            response = self.client.get(self.base_url + '/1')
            #print('User:', user, 'Expected Response:', user_response[user], 'Actual Response:', response.status_code)
            assert response.status_code == user_response[user]

    def test_post(self):
        """ 
        POST: /featuretodo
        User Roles: Employee, Administrator
        """
        data = dict(user_id=1, feature_id=1, priority=2, todo='Fix the database URL')
        response = self.client.post(self.base_url, data=json.dumps(data), content_type='application/json')
        assert response.status_code == 403
        user_response = dict(client=403, employee=201, admin=201)
        for user in user_response:
            self.client.get('/login_test/' + user)
            response = self.client.post(self.base_url, data=json.dumps(data), content_type='application/json')
            #print('User:', user, 'Expected Response:', user_response[user], 'Actual Response:', response.status_code)
            assert response.status_code == user_response[user]


class FeatureNoteTest(MyTest):
    base_url = '/featurenote'
    def test_get(self):
        """ 
        GET: /featurenote
        User Roles: Employee, Administrator
        """
        # Test getting all users
        response = self.client.get(self.base_url)
        assert response.status_code == 403
        user_response = dict(client=403, employee=200, admin=200)
        for user in user_response:
            self.client.get('/login_test/' + user)
            response = self.client.get(self.base_url)
            assert response.status_code == user_response[user]
        response = self.client.get('/logout')
        # Test for the retrieval of one user
        response = self.client.get(self.base_url + '/1')
        assert response.status_code == 403
        user_response = dict(client=403, employee=200, admin=200)
        for user in user_response:
            self.client.get('/login_test/' + user)
            response = self.client.get(self.base_url + '/1')
            #print('User:', user, 'Expected Response:', user_response[user], 'Actual Response:', response.status_code)
            assert response.status_code == user_response[user]

    def test_post(self):
        """ 
        POST: /featurenote
        User Roles: Employee, Administrator
        """
        data = dict(user_id=1, feature_id=1, note='May be willing to start a new project with us.')
        response = self.client.post(self.base_url, data=json.dumps(data), content_type='application/json')
        assert response.status_code == 403
        user_response = dict(client=403, employee=201, admin=201)
        for user in user_response:
            self.client.get('/login_test/' + user)
            response = self.client.post(self.base_url, data=json.dumps(data), content_type='application/json')
            #print('User:', user, 'Expected Response:', user_response[user], 'Actual Response:', response.status_code)
            assert response.status_code == user_response[user]

