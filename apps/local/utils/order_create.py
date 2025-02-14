def create_order(request,form,local,formset,extra_formset):
    order = form.save(commit=False)
    order.local=local
    order.created_user_pk=request.user.pk
    order.created_user_username=request.user.username
    order.created_user_email=request.user.email
    order.save()
    
    for object in formset:
        if object:
            item = object.save(commit=False)
            item.order = order
            item.price = item.service.price
            item.save()

    for extra_object in extra_formset:
                item = extra_object.save(commit=False)
                item.order = order
                print(item.description)
                print(item.price)
                if item.description is not None and item.price is not None:
                    item.save()
                
    