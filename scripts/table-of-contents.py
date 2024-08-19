import os
import pathlib
import nbformat
from nbconvert import NotebookExporter
from nbconvert.preprocessors import ExecutePreprocessor

REL_PATH = pathlib.Path("/root/mtg-modeling/notebooks/00-intro/00-00-table-of-contents.ipynb")

def _parse_name(name, loc=1):
    title = name.split('-')[:loc]
    title = ' '.join(title).upper()
    return title

def _parse_id(name, loc=1):
    file_id = name.split('-')[loc:]
    file_id = ' '.join(file_id).upper()
    return file_id


class SectionMetadata:
    def __init__(self, path):
        path = pathlib.Path(path)

        self.path = path
        self.dirname = path.name
        self.dir_id = self._parse_dirname()
        self.title = self._parse_dir_id()

    def __repr__(self):
        return f"SectionMetadata({self.path}, {self.dir_id}, {self.title})"

    def __str__(self):
        return f"{self.dir_id} {self.title}"
  
    def _parse_dirname(self):
        return _parse_name(self.dirname, loc=1)

    def _parse_dir_id(self):
        return _parse_id(self.dirname, loc=1)
    

class NotebookMetadata:
    def __init__(self, path):
        path = pathlib.Path(path) 

        self.path = path
        self.filename = path.stem
        self.directory = SectionMetadata(path.parent)
        self.file_id = self._parse_filename()
        self.title = self._parse_file_id()
        self.summary = self._extract_summary()
        self.rel_path = self.path.resolve().relative_to(REL_PATH.parent, walk_up=True)

    def __repr__(self):
        return f"NotebookMetadata({self.path}, {self.filename}, {self.file_id}, {self.title}, {self.summary})"

    def __str__(self):
        if self.summary:
            return f"{self.file_id} [{self.title}]({self.rel_path}): {self.summary}"
        else:
            return f"{self.file_id} [{self.title}]({self.rel_path})"

    def _parse_filename(self):
        return _parse_name(self.filename, loc=2)

    def _parse_file_id(self):
        return _parse_id(self.filename, loc=2)


    def _extract_summary(self):

        with open(self.path, 'r', encoding='utf-8') as f:
            nb = nbformat.read(f, as_version=4)

        for cell in nb.cells:
            if cell.cell_type == 'markdown':
                lines = cell.source.splitlines()
                for i, line in enumerate(lines):
                    if line.strip() == '# Summary':
                        return '\n'.join(lines[i+1:]).strip()

        return None


class TableOfContents:
    def __init__(self, root):
        self.root_dir = root
        self._files = []
        self.add_files()
        self.toc = self.compile_toc()

    def add_files(self):
        for dirpath, dirnames, filenames in os.walk(self.root_dir):
            dirnames.sort()
            filenames.sort()
            for filename in filenames:
                if filename.endswith('.ipynb'):
                    notebook_path = os.path.join(dirpath, filename)
                    print(notebook_path)
                    self._files.append(NotebookMetadata(notebook_path))


    def compile_toc(self):

        text = ["# Table of Contents\n"]
        prev_section = SectionMetadata('')
        for notebook in self._files:
            section = notebook.directory
            if section.dirname != prev_section.dirname:
                text.append(f"- __{section}__\n")
                prev_section = section

            text.append(f"  - {notebook}\n")
        return ''.join(text)
    
    def write_toc(self):
        with open(REL_PATH, 'r', encoding='utf-8') as f:
            nb = nbformat.read(f, as_version=4)
        

        # Check if the cell at the index is a code cell or markdown cell
        for cell_index, cell in enumerate(nb.cells):
            if cell.cell_type == 'markdown':
                if cell.source.startswith('# Table of Contents'):
                    print("Found Table of Contents cell")
                    nb.cells[cell_index].source = self.toc
                    print(nb.cells[0].source)

        # Execute the notebook to ensure everything is run and up-to-date
        ep = ExecutePreprocessor(timeout=600, kernel_name='python3')
        ep.preprocess(nb, {'metadata': {'path': REL_PATH.parent}})
        

        # Save the modified notebook
        with open(REL_PATH, 'w', encoding='utf-8') as f:
            nbformat.write(nb, f)

if __name__ == "__main__":
    cwd = pathlib.Path(os.getcwd())
    print("Working directory:", cwd)
    root_dir = pathlib.Path('/root/mtg-modeling/notebooks').relative_to(cwd, walk_up=True)
    print("Root directory:", root_dir)
    toc = TableOfContents(root_dir)
    print(toc.toc)
    toc.write_toc()
