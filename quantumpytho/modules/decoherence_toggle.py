class DecoherenceController:
    """
    Logical decoherence toggle.
    You can later wire this into a Qiskit Aer noise model or IBM backend selection.
    """

    def __init__(self):
        self.enabled = False

    def toggle(self) -> bool:
        self.enabled = not self.enabled
        state = "ON" if self.enabled else "OFF"
        print(f"\nQuantum Decoherence now [{state}]")
        return self.enabled
