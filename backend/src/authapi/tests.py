import json

from django.test import TestCase
from rest_framework.test import APIClient
from knox.models import AuthToken

from .models import UserAccount, UserPermissions


class UserAccountManagerTestCase(TestCase):
    @classmethod
    def setUpTestData(cls):
        # Create test user
        UserAccount.objects.create_user(
            username='testuser',
            email='testuser@test.test',
            visiblename='testuser',
            studentid='0000',
            password='testpassword',
        )

        # Create test superuser
        UserAccount.objects.create_superuser(
            username='testsuperuser',
            email='testsuperuser@test.test',
            visiblename='testsuperuser',
            password='testsuperpassword',
        )

    def test_user_creation(self):
        user = UserAccount.objects.get(username='testuser')
        self.assertEqual(user.username, 'testuser')
        self.assertEqual(user.email, 'testuser@test.test')
        self.assertEqual(user.visiblename, 'testuser')
        self.assertEqual(user.studentid, '0000')
        self.assertEqual(user.is_active, False)
        self.assertEqual(user.is_staff, False)
        self.assertEqual(user.permission, UserPermissions.USER)
        self.assertTrue(user.check_password('testpassword'))

        self.assertEqual(str(user), f'{user.studentid} {user.visiblename} @{user.username}')
        self.assertEqual(user.has_perm('some_permission'), False)
        self.assertEqual(user.has_module_perms('some_module'), True)

    def test_superuser_creation(self):
        user = UserAccount.objects.get(username='testsuperuser')
        self.assertEqual(user.username, 'testsuperuser')
        self.assertEqual(user.email, 'testsuperuser@test.test')
        self.assertEqual(user.visiblename, 'testsuperuser')
        self.assertEqual(user.studentid, '')
        self.assertEqual(user.is_active, True)
        self.assertEqual(user.is_staff, True)
        self.assertEqual(user.permission, UserPermissions.OTHER)
        self.assertTrue(user.check_password('testsuperpassword'))

        self.assertEqual(str(user), f'{user.studentid} {user.visiblename} @{user.username}')
        self.assertEqual(user.has_perm('some_permission'), True)
        self.assertEqual(user.has_module_perms('some_module'), True)

    @classmethod
    def tearDownClass(cls):
        UserAccount.objects.all().delete()
        UserAccount.objects.all().delete()


class RegisterAPITestCase(TestCase):
    @classmethod
    def setUpTestData(cls):
        # User with invalid info
        UserAccount.objects.create_user(
            username='inva',
            visiblename='li',
            email='dinfo@invalid.info',
            studentid='0000',
            password='testpassword',
        )

    def setUp(self):
        self.client = APIClient()

    def test_register_api_invalid_info(self):
        response = self.client.post('/auth/register/', {
            'username': 'inva',
            'visiblename': 'li',
            'email': 'dinfo@invalid.info',
            'password': 'invalid',
            'password_chk': 'info',
        }, format='json')

        response_body = json.loads(response.content)
        response_code = response.status_code
        self.assertEqual(response_code, 400)
        self.assertIn('아이디는 5자 이상이어야 합니다.', response_body['message'])
        self.assertIn('이름은 3자 이상이어야 합니다.', response_body['message'])
        self.assertIn('비밀번호는 8자 이상이어야 합니다.', response_body['message'])
        self.assertIn('비밀번호가 일치하지 않습니다.', response_body['message'])
        self.assertIn('이메일 사용자명이 학번이 아닙니다. 가입을 원할 경우 관리자에게 문의하세요.', response_body['message'])
        self.assertIn('학교 이메일이 아닙니다.', response_body['message'])
        self.assertIn('이미 존재하는 아이디입니다.', response_body['message'])
        self.assertIn('이미 존재하는 이메일입니다.', response_body['message'])
        self.assertIn('이미 존재하는 이름입니다.', response_body['message'])

    def test_register_api_valid_info(self):
        response = self.client.post('/auth/register/', {
            'username': 'valid',
            'visiblename': 'valid',
            'email': '999999@bjungang.hs.kr',
            'password': 'validpassword',
            'password_chk': 'validpassword',
        }, format='json')

        response_code = response.status_code
        self.assertEqual(response_code, 200)

        user = UserAccount.objects.get(username='valid')
        self.assertEqual(user.username, 'valid')
        self.assertEqual(user.visiblename, 'valid')
        self.assertEqual(user.email, '999999@bjungang.hs.kr')
        self.assertEqual(user.studentid, '9999')
        self.assertEqual(user.is_active, False)
        self.assertEqual(user.is_staff, False)
        self.assertEqual(user.permission, UserPermissions.USER)
        self.assertTrue(user.check_password('validpassword'))

    @classmethod
    def tearDownClass(cls):
        UserAccount.objects.all().delete()


class LoginAPITestCase(TestCase):
    @classmethod
    def setUpTestData(cls):
        # Create test user
        testuser = UserAccount.objects.create_user(
            username='testuser',
            email='testuser@test.test',
            visiblename='testuser',
            studentid='0000',
            password='validpassword',
        )
        testuser.is_active = True
        testuser.save()

        # Create test banned user
        banneduser = UserAccount.objects.create_user(
            username='banneduser',
            email='banneduser@test.test',
            visiblename='banneduser',
            studentid='9999',
            password='validpassword',
        )
        banneduser.is_blocked = True
        banneduser.is_active = True
        banneduser.save()

    def setUp(self):
        self.client = APIClient()

    def test_login_api_invalid_info(self):
        response = self.client.post('/auth/login/', {
            'username': 'testuser',
            'password': 'invalidpassword',
        }, format='json')

        response_body = json.loads(response.content)
        response_code = response.status_code
        self.assertEqual(response_code, 400)
        self.assertIn('비밀번호가 틀렸거나 존재하지 않는 계정입니다.', response_body['message'])

    def test_login_api_banned_user(self):
        response = self.client.post('/auth/login/', {
            'username': 'banneduser',
            'password': 'validpassword',
        }, format='json')

        response_body = json.loads(response.content)
        response_code = response.status_code
        self.assertEqual(response_code, 400)
        self.assertIn('서비스 이용이 정지된 계정입니다.', response_body['message'])

    def test_login_api_valid_info(self):
        response = self.client.post('/auth/login/', {
            'username': 'testuser',
            'password': 'validpassword',
        }, format='json')

        response_body = json.loads(response.content)
        response_code = response.status_code
        self.assertEqual(response_code, 200)
        self.assertIn('token', response_body)

    @classmethod
    def tearDownClass(cls):
        UserAccount.objects.all().delete()
        UserAccount.objects.all().delete()


class LogoutAPITestCase(TestCase):
    @classmethod
    def setUpTestData(cls):
        # Create test user
        testuser = UserAccount.objects.create_user(
            username='testuser',
            email='testuser@test.test',
            visiblename='testuser',
            studentid='0000',
            password='validpassword',
        )
        testuser.is_active = True
        testuser.save()

    def setUp(self):
        user = UserAccount.objects.get(username='testuser')
        self.token = AuthToken.objects.create(user)[1]

        self.client = APIClient()
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token)

    def test_logout_api(self):
        response = self.client.post('/auth/logout/', format='json')

        response_code = response.status_code
        self.assertEqual(response_code, 204)
        self.assertFalse(AuthToken.objects.filter(token_key=self.token).exists())

    @classmethod
    def tearDownClass(cls):
        UserAccount.objects.all().delete()

class UserAPITestCase(TestCase):
    @classmethod
    def setUpTestData(cls):
        # Create test user
        testuser = UserAccount.objects.create_user(
            username='testuser',
            email='testuser@test.test',
            visiblename='testuser',
            studentid='0000',
            password='validpassword',
        )
        testuser.is_active = True
        testuser.save()

        # Create other user
        otheruser = UserAccount.objects.create_user(
            username='otheruser',
            email='otheruser@test.test',
            visiblename='otheruser',
            studentid='9999',
            password='validpassword',
        )
        otheruser.is_active = True
        otheruser.save()

    def setUp(self):
        user = UserAccount.objects.get(username='testuser')
        self.token = AuthToken.objects.create(user)[1]

        self.client = APIClient()
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token)

    def test_user_api_self(self):
        response = self.client.get('/auth/user/', format='json')

        response_body = json.loads(response.content)
        response_code = response.status_code
        self.assertEqual(response_code, 200)

        self.assertIn('userid', response_body)
        self.assertIn('username', response_body)
        self.assertIn('visiblename', response_body)
        self.assertIn('email', response_body)
        self.assertIn('permission', response_body)
        self.assertIn('studentid', response_body)
        self.assertIn('profileimage', response_body)
        self.assertIn('description', response_body)
        self.assertIn('date_joined', response_body)
        self.assertIn('date_lastlogin', response_body)
        self.assertIn('is_blocked', response_body)
        self.assertIn('is_blocked_anon', response_body)
        self.assertIn('block_reason', response_body)
        self.assertIn('agreement_status', response_body)
        self.assertIn('post_count', response_body)
        self.assertIn('reply_count', response_body)

    def test_user_api_other(self):
        user = UserAccount.objects.get(username='otheruser')
        response = self.client.get('/auth/user/', {
            'userid': user.userid,
        }, format='json')

        response_body = json.loads(response.content)
        response_code = response.status_code
        self.assertEqual(response_code, 200)

        self.assertIn('userid', response_body)
        self.assertIn('username', response_body)
        self.assertIn('visiblename', response_body)
        self.assertIn('permission', response_body)
        self.assertIn('studentid', response_body)
        self.assertIn('profileimage', response_body)
        self.assertIn('description', response_body)
        self.assertIn('post_count', response_body)
        self.assertIn('reply_count', response_body)

        self.assertNotIn('email', response_body)
        self.assertNotIn('date_joined', response_body)
        self.assertNotIn('date_lastlogin', response_body)
        self.assertNotIn('is_blocked', response_body)
        self.assertNotIn('is_blocked_anon', response_body)
        self.assertNotIn('block_reason', response_body)
        self.assertNotIn('agreement_status', response_body)

    @classmethod
    def tearDownClass(cls):
        UserAccount.objects.all().delete()
        UserAccount.objects.all().delete()
