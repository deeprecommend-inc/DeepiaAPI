# Many to many CRUD operations

Child

```py
class Log(models.Model):
    prompt = models.CharField(
        max_length=128, blank=False, null=False)
    link = models.URLField(
        max_length=512, blank=False, null=False)
```

Parent

```py
class Category(models.Model):
    name = models.CharField(max_length=32, blank=False, null=False)
    user_id = models.IntegerField(blank=False, null=False)
    logs = models.ManyToManyField(Log, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
```

## Get the Log elements of a given Category

```py
Category.objects.get(id=[?]).logs.all()
```

## Fetch category detail

```py
category_detail = Category.objects.get(id=[?])
```

## Create and add Log element to Category

```py
category_detail.logs.create(...objects)
```

## Get all Category elements that have amenity id=3

```py
Category.objects.filter(logs__id=3)
```

# Many to many ManyToManyField reverse query create, read, update and delete operations with \_set syntax

## import

```py
from log.models import Log
from category.models import Category
```

## fetch detail

```py
log_detail = Log.objects.get(id=[?])
```

# Fetch all Category records with Log detail

```py
log_detail.category_set.all()
```

# Get the total Category count for the Log detail

```py
log_detail.category_set.count()
```

# Fetch Category records that match a filter with the Log detail

```py
log_detail.category_set.filter(log__startswith=[?])
```

# Create a Category directly with the Log detail

# NOTE: Django also supports the get_or_create() and update_or_create() operations

```py
log_detail.category_set.create(name=[?], user_id=[?])
```

# Create a Category separately and then add the Wifi Amenity to it

```py
new_category = Category(name='')
new_category.save()
log_detail.category_set.add(new_category)
```

# Create copy of breakfast items for later

```py
category_details = [ws for ws in log_detail.category_set.all()]
```

# Clear all the Wifi amenity records in the junction table for all Category elements

```py
log_detail.category_set.clear()
```

# Verify Wifi count is now 0

```py
log_detail.category_set.count()
```

# Reassign Wifi set from copy of Category elements

```py
log_detail.category_set.set(category_detail)
```

# Verify Item count is now back to original count

```py
log_detail.category_set.count()
6
```

# Reassign Store set from copy of wifi stores

```py
log_detail.category_set.set(category_detail)
```

# Clear the Wifi amenity record from the junction table for a certain Store element

category_to_remove_log = Category.objects.get(name\_\_startwith=[])
log_detail.category_set.remove(store_to_remove_amenity)
