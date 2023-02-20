import json

from django.test import TestCase
from rest_framework.test import APIClient
from knox.models import AuthToken

from authapi.models import UserAccount
from noticeapi.models import Notice
from communityapi.models import Post

from .models import Reply


class LikeAPITestCase(TestCase):
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

        # Create test notice
        cls.notice = Notice.objects.create(
            author=testuser,
            title='testnotice',
            document='testnotice',
        )

        # Create test post
        cls.post = Post.objects.create(
            author=testuser,
            title='testpost',
            document='testpost',
        )

    def setUp(self):
        user = UserAccount.objects.get(username='testuser')
        self.token = AuthToken.objects.create(user)[1]

        self.client = APIClient()
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token)

    def test_like_notice_post(self):
        # Like
        response = self.client.post(
            '/bbsbase/like/',
            {},
            format='json',
            QUERY_STRING='where=notice&id=' + str(self.notice.noticeid)
            )
        self.assertEqual(response.status_code, 200)

        self.notice.refresh_from_db()
        self.assertEqual(self.notice.likes.count(), 1)

        # Unlike
        response = self.client.post(
            '/bbsbase/like/',
            {},
            format='json',
            QUERY_STRING='where=notice&id=' + str(self.notice.noticeid)
            )
        self.assertEqual(response.status_code, 200)

        self.notice.refresh_from_db()
        self.assertEqual(self.notice.likes.count(), 0)

    def test_like_community_post(self):
        # Like
        response = self.client.post(
            '/bbsbase/like/',
            {},
            format='json',
            QUERY_STRING='where=community_post&id=' + str(self.post.postid)
            )
        self.assertEqual(response.status_code, 200)

        self.post.refresh_from_db()
        self.assertEqual(self.post.likes.count(), 1)

        # Unlike
        response = self.client.post(
            '/bbsbase/like/',
            {},
            format='json',
            QUERY_STRING='where=community_post&id=' + str(self.post.postid)
            )
        self.assertEqual(response.status_code, 200)

        self.post.refresh_from_db()
        self.assertEqual(self.post.likes.count(), 0)

    def test_like_notice_get(self):
        user = UserAccount.objects.get(username='testuser')

        # Clear likes
        self.notice.likes.clear()
        response = self.client.get(
            '/bbsbase/like/',
            {
                'where': 'notice',
                'id': self.notice.noticeid,
            },
            format='json',
            )
        self.assertEqual(response.status_code, 200)

        self.notice.refresh_from_db()
        self.assertEqual(self.notice.likes.count(), 0)

        # Add likes
        self.notice.likes.add(user)

        response = self.client.get(
            '/bbsbase/like/',
            {
                'where': 'notice',
                'id': self.notice.noticeid,
            },
            format='json',
            )
        self.assertEqual(response.status_code, 200)

        self.notice.refresh_from_db()
        self.assertEqual(self.notice.likes.count(), 1)

    def test_like_community_post_get(self):
        user = UserAccount.objects.get(username='testuser')

        # Clear likes
        self.post.likes.clear()
        response = self.client.get(
            '/bbsbase/like/',
            {
                'where': 'community_post',
                'id': self.post.postid,
            },
            format='json',
            )
        self.assertEqual(response.status_code, 200)

        self.post.refresh_from_db()
        self.assertEqual(self.post.likes.count(), 0)

        # Add likes
        self.post.likes.add(user)

        response = self.client.get(
            '/bbsbase/like/',
            {
                'where': 'community_post',
                'id': self.post.postid,
            },
            format='json',
            )
        self.assertEqual(response.status_code, 200)

        self.post.refresh_from_db()
        self.assertEqual(self.post.likes.count(), 1)

    def test_like_post_invalid(self):
        # Invalid parameters
        response = self.client.post(
            '/bbsbase/like/',
            {},
            format='json',
            QUERY_STRING='where=invalid&id=' + str(self.notice.noticeid)
            )

        self.assertEqual(response.status_code, 400)
        response_body = json.loads(response.content)

        self.assertEqual(response_body['message'], 'Invalid parameters')

        # Missing parameters
        response = self.client.post(
            '/bbsbase/like/',
            {},
            format='json',
            )

        self.assertEqual(response.status_code, 400)
        response_body = json.loads(response.content)

        self.assertEqual(response_body['message'], 'Missing parameters')

        # Non-existent object
        response = self.client.post(
            '/bbsbase/like/',
            {},
            format='json',
            QUERY_STRING='where=notice&id=999'
            )

        self.assertEqual(response.status_code, 404)
        response_body = json.loads(response.content)

        self.assertEqual(response_body['message'], 'Matching object not found')

    def test_like_get_invalid(self):
        # Invalid parameters
        response = self.client.get(
            '/bbsbase/like/',
            {
                'where': 'invalid',
                'id': self.notice.noticeid,
            },
            format='json',
            )

        self.assertEqual(response.status_code, 400)
        response_body = json.loads(response.content)

        self.assertEqual(response_body['message'], 'Invalid parameters')

        # Missing parameters
        response = self.client.get(
            '/bbsbase/like/',
            {},
            format='json',
            )

        self.assertEqual(response.status_code, 400)
        response_body = json.loads(response.content)

        self.assertEqual(response_body['message'], 'Missing parameters')

        # Non-existent object
        response = self.client.get(
            '/bbsbase/like/',
            {
                'where': 'notice',
                'id': 999,
            },
            format='json',
            )

        self.assertEqual(response.status_code, 404)
        response_body = json.loads(response.content)

        self.assertEqual(response_body['message'], 'Matching object not found')

    @classmethod
    def tearDownClass(cls):
        UserAccount.objects.all().delete()
        Notice.objects.all().delete()
        Post.objects.all().delete()


class ReplyTestCase(TestCase):
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

        # Create reply
        cls.reply = Reply.objects.create(
            author=testuser,
            text='test reply',
        )

        # Create reply with long text
        cls.longreply = Reply.objects.create(
            author=testuser,
            text='test reply' * 100,
        )

    def test_reply___str__(self):
        self.assertEqual(str(self.reply), '@testuser: test reply')
        self.assertEqual(str(self.longreply), '@testuser: test replytest reply')

    @classmethod
    def tearDownClass(cls):
        UserAccount.objects.all().delete()
        Reply.objects.all().delete()

class ReplyAPITestCase(TestCase):
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

        # Create test post
        cls.post = Post.objects.create(
            author=testuser,
            title='testpost',
            document='testpost',
        )

        # Create test notice
        cls.notice = Notice.objects.create(
            author=testuser,
            title='testnotice',
            document='testnotice',
        )

        # Create test reply
        cls.reply = Reply.objects.create(
            author=testuser,
            text='test reply',
        )

        # Add reply to notice, post
        cls.notice.replies.add(cls.reply)
        cls.post.replies.add(cls.reply)

        # Create test subreply
        cls.subreply = Reply.objects.create(
            author=testuser,
            text='test subreply',
        )
        cls.reply.replies.add(cls.subreply)

    def setUp(self):
        user = UserAccount.objects.get(username='testuser')
        self.token = AuthToken.objects.create(user)[1]

        self.client = APIClient()
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token)

    def test_reply_community_post_get(self):
        response = self.client.get(
            '/bbsbase/reply/',
            {
                'where': 'community_post',
                'id': self.post.postid,
            },
            format='json',
            )
        self.assertEqual(response.status_code, 200)

        response_body = json.loads(response.content)
        self.assertEqual(len(response_body), 1)

        self.assertIn('replyid', response_body[0])
        self.assertIn('author', response_body[0])
        self.assertIn('created', response_body[0])
        self.assertIn('modified', response_body[0])
        self.assertIn('text', response_body[0])
        self.assertIn('replies', response_body[0])
        self.assertIn('reply_count', response_body[0])

        self.assertEqual(response_body[0]['replyid'], self.reply.replyid)

    def test_reply_notice_get(self):
        response = self.client.get(
            '/bbsbase/reply/',
            {
                'where': 'notice',
                'id': self.notice.noticeid,
            },
            format='json',
            )
        self.assertEqual(response.status_code, 200)

        response_body = json.loads(response.content)
        self.assertEqual(len(response_body), 1)

        self.assertIn('replyid', response_body[0])
        self.assertIn('author', response_body[0])
        self.assertIn('created', response_body[0])
        self.assertIn('modified', response_body[0])
        self.assertIn('text', response_body[0])
        self.assertIn('replies', response_body[0])
        self.assertIn('reply_count', response_body[0])

        self.assertEqual(response_body[0]['replyid'], self.reply.replyid)

    def test_reply_reply_get(self):
        response = self.client.get(
            '/bbsbase/reply/',
            {
                'where': 'reply',
                'id': self.reply.replyid,
            },
            format='json',
            )
        self.assertEqual(response.status_code, 200)

        response_body = json.loads(response.content)
        self.assertEqual(len(response_body), 1)

        self.assertIn('replyid', response_body[0])
        self.assertIn('author', response_body[0])
        self.assertIn('created', response_body[0])
        self.assertIn('modified', response_body[0])
        self.assertIn('text', response_body[0])
        self.assertIn('replies', response_body[0])
        self.assertIn('reply_count', response_body[0])

        self.assertEqual(response_body[0]['replyid'], self.subreply.replyid)

    def test_reply_get_invalid(self):
        # Invalid parameters
        response = self.client.get(
            '/bbsbase/reply/',
            {
                'where': 'invalid',
                'id': self.post.postid,
            },
            format='json',
            )
        self.assertEqual(response.status_code, 400)

        response_body = json.loads(response.content)
        self.assertEqual(response_body['message'], 'Invalid parameters')

        # Missing parameters
        response = self.client.get(
            '/bbsbase/reply/',
            {},
            format='json',
            )
        self.assertEqual(response.status_code, 400)

        response_body = json.loads(response.content)
        self.assertEqual(response_body['message'], 'Missing parameters')\

        # Non-existent object
        response = self.client.get(
            '/bbsbase/reply/',
            {
                'where': 'community_post',
                'id': 999,
            },
            format='json',
            )
        self.assertEqual(response.status_code, 404)

        response_body = json.loads(response.content)
        self.assertEqual(response_body['message'], 'Matching object not found')

    def test_reply_get_recursively(self):
        response = self.client.get(
            '/bbsbase/reply/',
            {
                'where': 'community_post',
                'id': self.post.postid,
                'depth': 1,
            },
            format='json',
            )
        self.assertEqual(response.status_code, 200)

        response_body = json.loads(response.content)
        self.assertEqual(len(response_body), 1)

        self.assertIn('replyid', response_body[0])
        self.assertIn('author', response_body[0])
        self.assertIn('created', response_body[0])
        self.assertIn('modified', response_body[0])
        self.assertIn('text', response_body[0])
        self.assertIn('replies', response_body[0])
        self.assertIn('reply_count', response_body[0])

        self.assertEqual(len(response_body[0]['replies']), 1)
        self.assertEqual(response_body[0]['replies'][0]['replyid'], self.subreply.replyid)

    @classmethod
    def tearDownClass(cls):
        UserAccount.objects.all().delete()
        Post.objects.all().delete()
        Reply.objects.all().delete()
