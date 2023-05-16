from version2.backend.server import app

'''
개발 언어: Python 3.11
개발 환경: PyCharm
'''

version = '0.2.0'

if __name__ == '__main__':
    print('------------------------------------------------')
    print('capstone-designs CV - version ' + version)
    print('------------------------------------------------')

    app.run(host='0.0.0.0', port=9000)
