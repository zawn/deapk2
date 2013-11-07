import win32gui
import re
import win32process

class WindowMgr:
    """Encapsulates some calls to the winapi for window management"""
    def __init__ (self):
        """Constructor"""
        self._handle = None

    def find_window(self, class_name, window_name = None):
        """find a window by its class_name"""
        self._handle = win32gui.FindWindow(class_name, window_name)

    def _window_enum_callback(self, hwnd, wildcard):
        '''Pass to win32gui.EnumWindows() to check all the opened windows'''
        if re.match(wildcard, str(win32gui.GetWindowText(hwnd))) != None:
            self._handle = hwnd

    def find_window_wildcard(self, wildcard):
        self._handle = None
        win32gui.EnumWindows(self._window_enum_callback, wildcard)

    def set_foreground(self):
        """put the window in the foreground"""
        win32gui.SetForegroundWindow(self._handle)
        
    def get_foreground(self):
        return win32gui.GetWindowText(win32gui.GetForegroundWindow())
    
    def get_hwnds_for_hwnd (self,hw = None):
        if hw == None:
            hw = self._handle
            
        def callback (hwnd, hwnds):
            if win32gui.IsWindowVisible (hwnd):
                _, found_pid = win32process.GetWindowThreadProcessId (hwnd)
                if found_pid == pid:
                    hwnds.append (hwnd)
                return True
        _, pid = win32process.GetWindowThreadProcessId (hw)
        hwnds = []
        win32gui.EnumWindows (callback, hwnds)
        return hwnds
