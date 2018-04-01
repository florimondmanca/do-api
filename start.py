from subprocess import run

if __name__ == '__main__':
    run([
        'gunicorn',
        '--reload',
        'do.app',
    ])
