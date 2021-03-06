import logging
import subprocess
import shutil
from os.path import join, exists, split
from os import makedirs
from pylaroid.polaroid import SelfDevPhoto
from pylaroid.pdf import generate_pdf


class PhotoSheet(object):
    """Self developping photo sheet"""
    counter = 0
    paths = []
    polaroid = []
    generated = False
    photo_by_sheet = 5
    root_path = None
    logo = None

    def __init__(self, root_path):
        self.root_path = root_path
        if exists(join(root_path, 'options', 'logo.jpg')):
            self.logo = join(root_path, 'options', 'logo.jpg')
        for path in ['polaroid', 'pdf', 'original']:
            if not exists(join(root_path, path)):
                makedirs(join(root_path, path))

    def add_photo(self, file_path):
        if file_path not in self.paths:
            self.paths.append(file_path)
            self.generate_polaroid(file_path)
            self.move_original(file_path)
        if self.counter == self.photo_by_sheet:
            self.generate_sheet()
        else:
            need = self.photo_by_sheet - self.counter
            logging.info("Need %i more images for generate pdf\n\n" % need)
        if self.generated:
            self.reset()

    def move_original(self, file_path):
        split_path = split(file_path)
        new_path = join(split_path[0], 'original', split_path[1])
        shutil.move(file_path, new_path)
        logging.info("Original image moved to %s" % new_path)

    def generate_polaroid(self, file_path):
        image = SelfDevPhoto(file_path, logo=self.logo)
        self.polaroid.append(image.working_path)
        logging.info("Polaroid generated at %s" % image.working_path)
        self.counter += 1

    def print_pdf(self, pdf_path):
        logging.info("Printing pdf file: %s\n\n" % pdf_path)
        subprocess.call(['lpr', pdf_path])

    def generate_sheet(self):
        logging.info("We'll generate pdf sheet with: %s" %
                     "\n- ".join(self.polaroid))
        pdf_path = generate_pdf(self.polaroid, self.root_path)
        logging.info("Into pdf file: %s" % pdf_path)
        self.print_pdf(pdf_path)
        self.generated = True

    def reset(self):
        self.paths = []
        self.counter = 0
        self.generated = False
        self.polaroid = []
