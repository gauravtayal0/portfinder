import distutils.core
import sys
import textwrap


def main():
    requires = []
    scripts = []
    py_version = sys.version_info[:2]

    distutils.core.setup(
        name='portfinder',
        version='1.0.0',
        description='A library to choose unique available network ports.',
        long_description=textwrap.dedent("""\
          Portfinder provides an API to find and return an available network
          port for an application to bind to."""),
        package_dir={'': 'src'},
        platforms=['POSIX'],
        requires=requires,
        scripts=scripts


if __name__ == '__main__':
    main()