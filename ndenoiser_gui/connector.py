from tkinter import messagebox

class Connector:

    def ImportNDenoiser() -> bool:
        try:
            import neuroimage_denoiser as nd
        except ModuleNotFoundError:
            messagebox.showerror("Neuroimage Denoiser GUI", "Can't find the Neuroimage Denoiser module. Terminating")
            exit()
        return True