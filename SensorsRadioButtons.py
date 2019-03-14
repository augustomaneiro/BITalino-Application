import tkinter as tk

def chooseSensorAndSamplingRate():
    root = tk.Tk()
    root.title('BITalino')

    v = tk.StringVar()
    v.set("ACC")  # initializing the choice

    sr = tk.IntVar()
    sr.set(1000)  # initializing the choice


    sensors = [
        "ACC",
        "LUX",
        "ECG",
        "EMG",
        "EDA"
    ]

    samplingRates = [
        10,
        100,
        1000
    ]

    tk.Label(root,
             text="""Choose the sensor connected 
    to the BITalino board:""",
             justify = tk.LEFT,
             padx = 20).pack()

    for sensor in sensors:
        tk.Radiobutton(root,
                      text=sensor,
                      padx = 20,
                      variable=v,
                      value=sensor).pack(anchor=tk.W)

    tk.Label(root,
             text="""Choose the sampling rate (Hz):""",
             justify=tk.LEFT,
             padx = 20).pack()

    for sRate in samplingRates:
        tk.Radiobutton(root,
                       text=sRate,
                       variable=sr,
                       value=sRate).pack(anchor=tk.W)

    tk.Button(root,
              text = "Choose",
              justify = tk.CENTER,
              padx = 20,
              command = root.destroy,
              ).pack()

    root.mainloop()
    return v.get(), sr.get()
