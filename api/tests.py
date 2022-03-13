from django.test import TestCase
from django.urls import reverse
from api.models import (
    Folder,
    Document,
    Topic
)


class DocumentModelTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        # Set up non-modified objects used by all test methods
        folder_id = Folder.objects.create(folder_name="Test Folder Two")
        Document.objects.create(document_name='Test Document', folder_id=folder_id.id)

    def test_folder_name_label(self):
        folder = Folder.objects.get(id=1)
        field_label = folder._meta.get_field('folder_name').verbose_name
        self.assertEqual(field_label, 'Folder Name')

    def test_folder_name_max_length(self):
        folder = Folder.objects.get(id=1)
        max_length = folder._meta.get_field('folder_name').max_length
        self.assertEqual(max_length, 30)

    def test_folder_name_not_max_length(self):
        folder = Folder.objects.get(id=1)
        max_length = folder._meta.get_field('folder_name').max_length
        self.assertNotEqual(max_length, 100)

    def test_document_name_label(self):
        document = Document.objects.get(id=1)
        field_label = document._meta.get_field('document_name').verbose_name
        self.assertEqual(field_label, 'Document Name')

    def test_document_name_max_length(self):
        document = Document.objects.get(id=1)
        max_length = document._meta.get_field('document_name').max_length
        self.assertEqual(max_length, 30)

    def test_document_name_not_max_length(self):
        document = Document.objects.get(id=1)
        max_length = document._meta.get_field('document_name').max_length
        self.assertNotEqual(max_length, 100)

    # def test_document_folder_related_name(self):
    #     document = Document.objects.get(id=1)
    #     field_label = document._meta.get_field('folder').related_name
    #     self.assertEqual(field_label, 'available_documents')


class TopicModelTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        # Set up non-modified objects used by all test methods
        folder_id = Folder.objects.create(folder_name="Test Folder Three")
        document_id = Document.objects.create(document_name="Test Document Two", folder_id=folder_id.id)
        Topic.objects.create(
            topic_name='Test Topic',
            short_description="Test Short Description",
            long_description="Test Long Description",
            document_id=document_id.id,
        )

    def test_topic_name_label(self):
        topic = Topic.objects.get(id=1)
        field_label = topic._meta.get_field('topic_name').verbose_name
        self.assertEqual(field_label, 'Topic Name')

    def test_shot_description_label(self):
        topic = Topic.objects.get(id=1)
        field_label = topic._meta.get_field('short_description').verbose_name
        self.assertEqual(field_label, 'Short Topic Description')

    def test_long_description_label(self):
        topic = Topic.objects.get(id=1)
        field_label = topic._meta.get_field('long_description').verbose_name
        self.assertEqual(field_label, 'Long Topic Description')

    def test_topic_name_max_length(self):
        topic = Topic.objects.get(id=1)
        max_length = topic._meta.get_field('topic_name').max_length
        self.assertEqual(max_length, 256)

    def test_topic_name_not_max_length(self):
        topic = Topic.objects.get(id=1)
        max_length = topic._meta.get_field('topic_name').max_length
        self.assertNotEqual(max_length, 100)

    # def test_topic_folder_related_name(self):
    #     topic = Topic.objects.get(id=1)
    #     field_label = topic._meta.get_field('document').related_name
    #     self.assertEqual(field_label, 'available_topics')


# class FolderModelTest(TestCase):
#     @classmethod
#     def setUpTestData(cls):
#         # Set up non-modified objects used by all test methods
#         Folder.objects.create(folder_name='Test Folder')
#
#     def test_folder_name_label(self):
#         folder = Folder.objects.get(id=1)
#         field_label = folder._meta.get_field('folder_name').verbose_name
#         self.assertEqual(field_label, 'Folder Name')
#
#     def test_folder_name_max_length(self):
#         folder = Folder.objects.get(id=1)
#         max_length = folder._meta.get_field('folder_name').max_length
#         self.assertEqual(max_length, 30)
#
#     def test_folder_name_not_max_length(self):
#         folder = Folder.objects.get(id=1)
#         max_length = folder._meta.get_field('folder_name').max_length
#         self.assertNotEqual(max_length, 100)
