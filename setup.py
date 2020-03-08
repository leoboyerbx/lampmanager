from distutils.core import setup

setup(name="lampmanager",  # Name of the program.
      version="0.1",  # Version of the program.
      description="An easy-to-use interface to manage your LAMP stack.",  # You don't need any help here.
      author="leoboyerbx",  # Nor here.
      author_email="contact@leoboyer.fr",  # Nor here :D
      url="http://leoboyer.fr",  # If you have a website for you program.. put it here.
      license='GPLv3',  # The license of the program.
      scripts=['lampmanager-gui'],

      # Here you can choose where do you want to preinst your files on the local system, the "myprogram" file will be automatically installed in its correct place later, so you have only to choose where do you want to preinst the optional files that you shape with the Python script
      data_files=[("lib/myprogram", ["ui.glade"]),
                  # This is going to preinst the "ui.glade" file under the /usr/lib/myprogram path.
                  ("share/applications", [
                      "myprogram.desktop"])])  # And this is going to preinst the .desktop file under the /usr/share/applications folder, all the folder are automatically installed under the /usr folder in your root partition, you don't need to add "/usr/ to the path.
