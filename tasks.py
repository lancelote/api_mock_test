from invoke import task, run


@task
def syntax(ctx):
    ctx.run('python -m pylint src/ tests/')


@task
def tests(ctx, verbosity=1):
    ctx.run('python -m nose --verbosity=%s .' % verbosity)
