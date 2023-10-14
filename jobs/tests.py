from django.contrib.auth import get_user_model
from django.test import TestCase
from rest_framework.test import APIClient
from .models import Company, JobPosting

User = get_user_model()


class JobPostingTests(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.company = Company.objects.create(name='WantedLab', country='Korea', location='Seoul')
        self.user = User.objects.create(username='testuser', email='test@example.com')
        self.client.force_authenticate(user=self.user)

    def test_create_job_posting(self):
        # 채용공고를 등록
        url = '/api/v1/job-postings/'
        data = {
            'company': self.company.id,
            'position': 'Backend Developer',
            'reward': 1000000,
            'content': 'WantedLab is hiring a Backend Developer.',
            'skills': 'Python, Django'
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, 201)
        self.assertEqual(JobPosting.objects.count(), 1)
        self.assertEqual(JobPosting.objects.get().position, 'Backend Developer')

    def test_update_job_posting(self):
        # 채용공고를 수정(회사 id 제외)
        obj = JobPosting.objects.create(
            company=self.company,
            position='Frontend Developer',
            reward=900000,
            content='WantedLab is hiring a Frontend Developer.',
            skills='JavaScript, React'
        )
        origin_company_id = obj.company_id
        url = f'/api/v1/job-postings/{obj.id}/'
        data = {
            'company': 3,
            'position': 'Backend Developer!!',
            'reward': 1000000,
            'content': 'WantedLab is hiring a Backend Developer.',
            'skills': 'Python, Django'
        }
        response = self.client.patch(url, data, format='json')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(JobPosting.objects.get().company_id, origin_company_id)
        self.assertEqual(JobPosting.objects.get().position, 'Backend Developer!!')
        self.assertEqual(JobPosting.objects.get().reward, 1000000)
        self.assertEqual(JobPosting.objects.get().content, 'WantedLab is hiring a Backend Developer.')
        self.assertEqual(JobPosting.objects.get().skills, 'Python, Django')

    def test_update_job_posting(self):
        # 채용공고를 삭제
        obj = JobPosting.objects.create(
            company=self.company,
            position='Frontend Developer',
            reward=900000,
            content='WantedLab is hiring a Frontend Developer.',
            skills='JavaScript, React'
        )
        obj_id = obj.id
        url = f'/api/v1/job-postings/{obj_id}/'

        response = self.client.delete(url, format='json')
        self.assertEqual(response.status_code, 204)
        with self.assertRaises(JobPosting.DoesNotExist):
            JobPosting.objects.get(id=obj_id)

    def test_list_job_postings(self):
        # 채용공고 목록 조회
        url = '/api/v1/job-postings/'
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

    def test_search_list_job_postings(self):
        # 채용공고 목록에서 키워드 검색
        url = f'/api/v1/job-postings/?search=python'
        JobPosting.objects.create(
            company=self.company,
            position='Frontend Developer',
            reward=900000,
            content='WantedLab is hiring a Frontend Developer.',
            skills='JavaScript, React'
        )
        JobPosting.objects.create(
            company=self.company,
            position='Backend Developer',
            reward=900000,
            content='WantedLab is hiring a Backend Developer.',
            skills='Python, Django'
        )
        JobPosting.objects.create(
            company=self.company,
            position='Backend Developer',
            reward=900000,
            content='WantedLab is hiring a Backend Developer.',
            skills='Python, Fast'
        )
        response = self.client.get(url)
        check_filtered = 0
        for data in response.data:
            for key in data:
                if 'python' in str(data[key]).lower():
                    check_filtered += 1
                    break
        self.assertEquals(check_filtered, len(response.data))
        self.assertEqual(response.status_code, 200)

    def test_detail_job_postings(self):
        # 채용공고 상세 조회(상세 조회 시 해당 회사의 다른 공고 아이디를 확인)
        obj = JobPosting.objects.create(
            company=self.company,
            position='Frontend Developer',
            reward=900000,
            content='WantedLab is hiring a Frontend Developer.',
            skills='JavaScript, React'
        )
        JobPosting.objects.create(
            company=self.company,
            position='Backend Developer',
            reward=900000,
            content='WantedLab is hiring a Backend Developer.',
            skills='Python, Django'
        )
        JobPosting.objects.create(
            company=self.company,
            position='ios Developer',
            reward=900000,
            content='WantedLab is hiring a ios Developer.',
            skills='swift'
        )
        url = f'/api/v1/job-postings/{obj.id}/'
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertIn('company_another_postings', response.data)
        self.assertEqual(len(response.data['company_another_postings']), 3)

    def test_apply_for_job(self):
        # 채용공고 지원
        job_posting = JobPosting.objects.create(
            company=self.company,
            position='Frontend Developer',
            reward=900000,
            content='WantedLab is hiring a Frontend Developer.',
            skills='JavaScript, React'
        )
        url = f'/api/v1/job-postings/{job_posting.id}/apply/'
        data = {'applicant': self.user.id}
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, 201)

    def test_list_apply_for_job(self):
        # 채용공고 목록 조회
        job_posting = JobPosting.objects.create(
            company=self.company,
            position='Frontend Developer',
            reward=900000,
            content='WantedLab is hiring a Frontend Developer.',
            skills='JavaScript, React'
        )
        url = f'/api/v1/job-postings/{job_posting.id}/apply/'
        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, 200)
