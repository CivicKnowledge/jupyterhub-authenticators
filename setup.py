from setuptools import setup

setup(
    name='jh-auth',
    version='0.1.5',
    description='Custom authenticators for JupyterHub',
    url='https://github.com/CivicKnowledge/jupyterhub-authenticators.git',
    author='Eric Busboom',
    author_email='eric@civicknowledge.com',
    license='2 Clause BSD',
    packages=['jhauth'],
    install_requires=['oauthenticator']
)
