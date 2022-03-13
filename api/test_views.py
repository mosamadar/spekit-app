from django.test import TestCase
from django.urls import reverse

from api.models import (
    Folder,
    Document,
    Topic
)

class FolderListViewTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        # Create 12 folders for tests
        number_of_folders = 13

        for folder_id in range(1, number_of_folders):
            Folder.objects.create(
                folder_name=f'Folder {folder_id}',
            )

    def test_view_url_exists_at_desired_location(self):
        response = self.client.get('/api/folders/')
        self.assertEqual(response.status_code, 200)

    def test_view_url_accessible_by_name(self):
        response = self.client.get(reverse('folders'))
        self.assertEqual(response.status_code, 200)


class DocumentListViewTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        # Create 12 documents for tests
        number_of_documents = 13

        for document_id in range(1, number_of_documents):
            folder = Folder.objects.create(
                folder_name=f'Folder {document_id}',
            )
            Document.objects.create(
                document_name=f'Document {document_id}',
                folder_id=folder.id,

            )

    def test_view_url_exists_at_desired_location(self):
        response = self.client.get('/api/documents/')
        self.assertEqual(response.status_code, 200)

    def test_view_url_accessible_by_name(self):
        response = self.client.get(reverse('documents'))
        self.assertEqual(response.status_code, 200)


class TopicListViewTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        # Create 12 topics for tests
        number_of_topics = 13

        for topic_id in range(1, number_of_topics):
            folder = Folder.objects.create(
                folder_name=f'Folder {topic_id}',
            )
            document = Document.objects.create(
                document_name=f'Document {topic_id}',
                folder_id=folder.id,

            )
            Topic.objects.create(
                topic_name=f'Topic {topic_id}',
                short_description=f'Test Short Description {topic_id}',
                long_description=f'Test Long Description {topic_id}',
                document_id=document.id,
            )

    def test_view_url_exists_at_desired_location(self):
        response = self.client.get('/api/topics/')
        self.assertEqual(response.status_code, 200)

    def test_view_url_accessible_by_name(self):
        response = self.client.get(reverse('topics'))
        self.assertEqual(response.status_code, 200)

    def test_find_document(self):
        # Get documents by desired params
        response = self.client.get(reverse('find_documents') + '?topic_name=Topic 2&folder_name=Folder 2')
        self.assertEqual(response.status_code, 201)
        # self.assertEqual(len(response.context['document_list']), 3)