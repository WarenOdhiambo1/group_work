# Gallery Setup with Image Links

## Model Configuration

The `Activity` model uses `image_url` field to store external image links (e.g., from Pinterest, Unsplash).

## Sample Image Links

```python
# Pinterest links for activities:
1. https://www.pinterest.com/pin/35606653299726149/
2. https://www.pinterest.com/pin/1011339660066185893/
3. https://www.pinterest.com/pin/50032245854265086/
4. https://www.pinterest.com/pin/678636237640439590/
5. https://www.pinterest.com/pin/116249234130017624/
6. https://www.pinterest.com/pin/307511480823438540/
```

## Populating Sample Data

Run in Django shell:
```bash
python manage.py shell
```

```python
from operations.sample_data import populate_activities
populate_activities()
```

## Adding Activities via Admin

1. Go to `/admin/`
2. Add Activity with name, type, price, description
3. Paste image URL in the `image_url` field
