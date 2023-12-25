import django_filters as filters
from todo.models import ToDoList
from django.db.models import Count, Case, When, BooleanField


class ToDoListFilter(filters.FilterSet):
    start_slug = filters.CharFilter(field_name='slug', lookup_expr='startswith')
    contain_slug = filters.CharFilter(field_name='slug', lookup_expr='contains')
    end_slug = filters.CharFilter(field_name='slug', lookup_expr='endswith')
    more_than_time_created = filters.DateFilter(field_name='created', lookup_expr='gt')
    less_than_time_created = filters.DateFilter(field_name='created', lookup_expr='lt')
    contain_hashags = filters.CharFilter(field_name='hashtags', lookup_expr='contains')
    more_than_comment = filters.NumberFilter(field_name='comments', method='get_count_gt_comments', label='more than count')
    less_than_comment = filters.NumberFilter(field_name='comments', method='get_count_lt_comments')
    exact_comment = filters.NumberFilter(field_name='comments', method='get_count_exact_comments')
    contain_description = filters.CharFilter(field_name='description', lookup_expr='contains')
    start_title = filters.CharFilter(field_name='title', lookup_expr='startswith')
    contain_title = filters.CharFilter(field_name='title', lookup_expr='contains')
    end_title = filters.CharFilter(field_name='title', lookup_expr='endswith')
    # with_icon = filters.BooleanFilter(field_name='icon', lookup_expr='isnull')

    more_than_item = filters.NumberFilter(field_name='items', method='get_count_gt_items', label='more than item')
    less_than_item = filters.NumberFilter(field_name='items', method='get_count_lt_items', label='less than item')


    # for items
    def get_count_items(self, queryset, field_name, value):
        return queryset.annotate(count_items=Count('items'))


    def get_count_lt_items(self, queryset, field_name, value):
        
        return self.get_count_items(queryset, field_name, value).filter(count_items__lt=value)
    

    def get_count_gt_items(self, queryset, field_name, value):
        queryset = self.get_count_items(queryset, field_name, value)
        for i in queryset:
            print(i.count_items)
        return queryset.filter(count_items__gt=value)
    
    
    # for comment
    def get_count_comments(self, queryset, field_name, value):
            return queryset.annotate(comments_count=Count('comments'))


    def get_count_gt_comments(self, queryset, field_name, value):
        return self.get_count_comments(queryset, field_name, value).filter(comments_count__gt=value)


    def get_count_lt_comments(self, queryset, field_name, value):
        return self.get_count_comments(queryset, field_name, value).filter(comments_count__lt=value)
    

    def get_count_exact_comments(self, queryset, field_name, value):
        return self.get_count_comments(queryset, field_name, value).filter(comments_count=value)
    

    # def filter_by_icon(self, queryst, field_name, value):
    #     print(value)
    #     queryst = queryst.annotate(
    #         icon_is_null=Case(When(icon__isnull=True, then=True),
    #                           default=False,
    #                           output_field=BooleanField())
    #     )
    #     return queryst.filter(icon_is_null=value)

    class Meta:
        model = ToDoList
        fields = ['slug', 'color', 'priority', 'more_than_time_created',
                  'less_than_time_created' ,'contain_hashags' ,'more_than_comment' ,
                  'less_than_comment' ,'exact_comment' ,'contain_description' ,
                  'start_title' ,'contain_title' ,'end_title' ,
                  'more_than_item' ,'less_than_item'
                  ]