import pytest
from rest_framework.test import APIClient
from ads.models import Ad, Category
from users.models import CustomUser

@pytest.mark.django_db
def test_recommended_ads_return_only_approved_and_recommended():
    user = CustomUser.objects.create(username='testuser')
    category = Category.objects.create(name="Тестова")
    
    Ad.objects.create(title="Не показати", is_recommended=True, status="draft", price=100, user=user)
    Ad.objects.create(title="Показати", is_recommended=True, status="approved", price=100, user=user, category=category)

    client = APIClient()
    response = client.get('/api/recommendations/')

    assert response.status_code == 200
    assert len(response.data) == 1
    assert response.data[0]['title'] == "Показати"