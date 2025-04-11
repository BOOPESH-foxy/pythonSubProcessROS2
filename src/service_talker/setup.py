from setuptools import find_packages, setup

package_name = 'service_talker'

setup(
    name=package_name,
    version='0.0.0',
    packages=find_packages(exclude=['test']),
    data_files=[
        ('share/ament_index/resource_index/packages',
            ['resource/' + package_name]),
        ('share/' + package_name, ['package.xml']),
    ],
    install_requires=['setuptools'],
    zip_safe=True,
    maintainer='roots',
    maintainer_email='boopesh.mc@gmail.com',
    description='TODO: Package description',
    license='Apache-2.0',
    tests_require=['pytest'],
    entry_points={
        'console_scripts': [
            'talker_trigger_node = service_talker.ros2_serviceCall:main',
        ],
    },
    package_data={
        'service_talker': ['ros2_commands.py'],
    },
)