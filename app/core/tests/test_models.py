from unittest.mock import patch

from django.test import TestCase
from django.contrib.auth import get_user_model

from core import models


def sample_user(email='test@parisdevelloper', password="test123"):
    return get_user_model().objects.create_user(email, password)


class ModelsTests(TestCase):

    def test_create_user_with_email_successful(self):
        email = "test@mail.com"
        password = "testpassword"
        user = get_user_model().objects.create_user(
            email=email,
            password=password
        )
        self.assertEqual(user.email, email)
        self.assertTrue(user.check_password(password))

    def test_new_user_normalize(self):
        email = 'test@PARIS.COM'
        user = get_user_model().objects.create_user(email, 'test123')
        self.assertEqual(user.email, email.lower())

    def test_new_user_invalid_email(self):
        with self.assertRaises(ValueError):
            get_user_model().objects.create_user(None, 'test123')

    def test_create_new_super_user(self):
        user = get_user_model().objects.create_superuser(
            'test@123.com',
            'test123', )
        self.assertTrue(user.is_superuser)
        self.assertTrue(user.is_staff)

    def test_tag_str(self):
        """Test the tag sting representation"""
        tag = models.Tag.objects.create(
            user = sample_user(),
            name = 'Vegan',

        )
        self.assertEqual(str(tag), tag.name)

    def test_ingredient_str(self):
        """Test the ingredient string representation """
        ingredient = models.Ingredient.objects.create(
            user=sample_user(),
            name='rice',

        )

        self.assertEqual(str(ingredient), ingredient.name)

    def test_recipe_str(self):
        recipe = models.Recipe.objects.create(
            user= sample_user(),
            title= 'Pasta and Steack',
            time_minutes=5,
            price=5.00,
        )
        self.assertEqual(str(recipe), recipe.title)

    @patch('uuid.uuid4')
    def test_recipe_file_name_uuid(self, mock_uuid):
        """Test that image is saved in the correct location"""
        uuid = 'test-uuid'
        mock_uuid.return_value = uuid
        file_path = models.recipe_image_file_path(None, 'myimage.jpg')
        expath = f"uploads/recipe/{uuid}.jpg"
        self.assertEqual(file_path, expath)
