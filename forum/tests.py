from django.test import TestCase
from accounts.models import PawMedicUser
from forum.models import ForumPost, Comment
from forum.forms import ForumCommentForm


class ForumPostModelTest(TestCase):
    def setUp(self):
        self.user = PawMedicUser.objects.create_user(
            username="forumuser",
            email="forum@example.com",
            password="TestPass123",
            first_name="Forum",
            last_name="User",
            is_active=True,
        )

    def test_create_forum_post(self):
        post = ForumPost.objects.create(
            author=self.user,
            title="My First Post",
            content="This is the content of my first forum post.",
        )
        self.assertEqual(post.title, "My First Post")
        self.assertEqual(post.author, self.user)


class CommentModelTest(TestCase):
    def setUp(self):
        self.user = PawMedicUser.objects.create_user(
            username="commenter",
            email="commenter@example.com",
            password="TestPass123",
            is_active=True,
        )
        self.post = ForumPost.objects.create(
            author=self.user, title="Test Post", content="Test content"
        )

    def test_create_comment(self):
        comment = Comment.objects.create(
            post=self.post, author=self.user, content="This is a test comment"
        )
        self.assertEqual(comment.content, "This is a test comment")
        self.assertEqual(comment.post, self.post)


class ForumCommentFormTest(TestCase):
    def test_valid_comment_form(self):
        form_data = {"content": "This is a valid comment"}
        form = ForumCommentForm(data=form_data)
        self.assertTrue(form.is_valid())

    def test_empty_comment_form(self):
        form_data = {"content": ""}
        form = ForumCommentForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertIn("content", form.errors)
