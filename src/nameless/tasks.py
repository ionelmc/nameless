from django_rq import job


@job
def stuff():
    raise NotImplementedError
