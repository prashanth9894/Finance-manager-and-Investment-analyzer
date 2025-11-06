from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('add/', views.add_transaction, name='add_transaction'),
    path('add-investment/', views.add_investment, name='add_investment'),
    path('investments/', views.analyze_investment, name='investments'),
    path('manage-investments/', views.manage_investments, name='manage_investments'),
    path('edit-investment/<int:row_id>/', views.edit_investment, name='edit_investment'),
    path('delete-investment/<int:row_id>/', views.delete_investment, name='delete_investment'),
    path('api/expense-chart/', views.expense_chart_data, name='expense_chart_data'),
    path('delete/<int:row_id>/', views.delete_transaction, name='delete_transaction'),
]