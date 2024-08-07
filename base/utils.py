
def obj_to_model_dump(obj):
  if obj:
    return obj.model_dump(exclude_none=True)
  else:
    return None
