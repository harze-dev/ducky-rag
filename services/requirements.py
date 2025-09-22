"""
Requirements service for managing requirements documents and project plans.
Handles all filesystem operations for the requirements workflow.
"""
from datetime import datetime
from pathlib import Path
from typing import List, Tuple, Optional


class RequirementsService:
    """Service for managing requirements documents and studio-generated plans"""

    def __init__(self):
        self.requirements_folder = Path("data/requirements")
        self.studio_folder = Path("data/requirements/studio")
        self._ensure_directories_exist()

    def _ensure_directories_exist(self):
        """Create requirements directories if they don't exist"""
        self.requirements_folder.mkdir(parents=True, exist_ok=True)
        self.studio_folder.mkdir(parents=True, exist_ok=True)

    def list_requirements_files(self) -> List[str]:
        """List all requirements documents in the requirements folder"""
        files = []
        if self.requirements_folder.exists():
            for file_path in self.requirements_folder.iterdir():
                if file_path.is_file() and file_path.suffix in ['.txt', '.md', '.doc', '.docx']:
                    files.append(file_path.name)
        return sorted(files)

    def list_studio_files(self) -> List[str]:
        """List all studio-generated plans in the studio folder"""
        files = []
        if self.studio_folder.exists():
            for file_path in self.studio_folder.iterdir():
                if file_path.is_file() and file_path.suffix in ['.txt', '.md', '.doc', '.docx']:
                    files.append(file_path.name)
        return sorted(files)

    def read_file_content(self, filename: str, is_studio_file: bool = False) -> Optional[str]:
        """
        Read content from a requirements or studio file

        Args:
            filename: Name of the file to read
            is_studio_file: True if file is in studio folder, False for requirements folder

        Returns:
            File content as string, or None if error
        """
        try:
            folder = self.studio_folder if is_studio_file else self.requirements_folder
            file_path = folder / filename
            with open(file_path, 'r', encoding='utf-8') as f:
                return f.read()
        except Exception as e:
            print(f"Error reading file {filename}: {str(e)}")
            return None

    def save_requirements_document(self, content: str, product_name: str, requirement_type: str) -> Tuple[bool, str]:
        """
        Save a requirements document to the requirements folder

        Args:
            content: Document content
            product_name: Name of the product
            requirement_type: Type of requirement document

        Returns:
            Tuple of (success: bool, filename: str)
        """
        try:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"{requirement_type.replace(' ', '_')}_{product_name.replace(' ', '_')}_{timestamp}.txt"
            file_path = self.requirements_folder / filename

            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(f"Product: {product_name}\n")
                f.write(f"Document Type: {requirement_type}\n")
                f.write(f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
                f.write("=" * 50 + "\n\n")
                f.write(content)

            return True, filename
        except Exception as e:
            print(f"Error saving requirements document: {str(e)}")
            return False, str(e)

    def save_project_plan(self, content: str, product_name: str, plan_type: str, num_source_docs: int) -> Tuple[bool, str]:
        """
        Save a project plan to the studio folder

        Args:
            content: Plan content
            product_name: Name of the product
            plan_type: Type of plan (e.g., "Engineering_Project_Plan", "Risk_Mitigation_Plan")
            num_source_docs: Number of source documents used

        Returns:
            Tuple of (success: bool, filename: str)
        """
        try:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"{plan_type}_{product_name.replace(' ', '_')}_{timestamp}.txt"
            file_path = self.studio_folder / filename

            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(f"Product: {product_name}\n")
                f.write(f"Document Type: {plan_type.replace('_', ' ')}\n")
                f.write(f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
                f.write(f"Based on {num_source_docs} requirements documents\n")
                f.write("=" * 50 + "\n\n")
                f.write(content)

            return True, filename
        except Exception as e:
            print(f"Error saving project plan: {str(e)}")
            return False, str(e)

    def get_all_requirements_content(self) -> Tuple[str, str]:
        """
        Read and combine all requirements documents

        Returns:
            Tuple of (combined_content: str, extracted_product_name: str)
        """
        all_requirements = ""
        product_name_extracted = "Unknown Product"

        requirements_files = self.list_requirements_files()

        for filename in requirements_files:
            content = self.read_file_content(filename, is_studio_file=False)
            if content:
                all_requirements += f"\n\n--- {filename} ---\n{content}"

                # Extract product name from first file
                if product_name_extracted == "Unknown Product" and content.startswith("Product:"):
                    lines = content.split('\n')
                    product_name_extracted = lines[0].replace("Product:", "").strip()

        return all_requirements, product_name_extracted

    def get_requirements_count(self) -> int:
        """Get the number of requirements documents"""
        return len(self.list_requirements_files())

    def get_studio_count(self) -> int:
        """Get the number of studio documents"""
        return len(self.list_studio_files())

    def clear_all_files(self) -> Tuple[bool, str]:
        """
        Clear all files from both requirements and studio folders

        Returns:
            Tuple of (success: bool, message: str)
        """
        try:
            deleted_count = 0

            # Clear requirements folder
            if self.requirements_folder.exists():
                for file_path in self.requirements_folder.iterdir():
                    if file_path.is_file() and file_path.suffix in ['.txt', '.md', '.doc', '.docx']:
                        file_path.unlink()
                        deleted_count += 1

            # Clear studio folder
            if self.studio_folder.exists():
                for file_path in self.studio_folder.iterdir():
                    if file_path.is_file() and file_path.suffix in ['.txt', '.md', '.doc', '.docx']:
                        file_path.unlink()
                        deleted_count += 1

            return True, f"Successfully deleted {deleted_count} files"

        except Exception as e:
            print(f"Error clearing files: {str(e)}")
            return False, f"Error clearing files: {str(e)}"


# Global instance for use across the application
requirements_service = RequirementsService()
