DIAGNOSTICS = {
    'missing_hole': {
        'severity': 'Critical',
        'consequence': (
            "Missing holes prevent component leads from being inserted and soldered, "
            "causing open circuits. In through-hole components like connectors or ICs, "
            "this means the component physically cannot be mounted, halting assembly entirely."
        ),
        'solution': (
            "Re-drill the missing hole using a CNC drill at the correct diameter specified "
            "in the PCB design file. Verify drill alignment against the Gerber file. "
            "After re-drilling, inspect pad integrity and re-plate if the annular ring is damaged."
        )
    },
    'mouse_bite': {
        'severity': 'High',
        'consequence': (
            "Mouse bites are irregular edge cuts that weaken the PCB mechanically and can "
            "sever edge traces or ground planes. This causes intermittent connections under "
            "vibration or thermal stress, leading to unpredictable field failures."
        ),
        'solution': (
            "If the mouse bite does not affect any trace, smooth the edge with a fine file "
            "and apply conformal coating to prevent oxidation. If a trace is severed, "
            "reroute using a wire bridge and secure with epoxy for mechanical strength."
        )
    },
    'open_circuit': {
        'severity': 'Critical',
        'consequence': (
            "An open circuit breaks the conductive path, meaning no current flows through "
            "that net. Depending on location this can disable an entire functional block — "
            "power delivery, signal lines, or ground return paths — rendering the board non-functional."
        ),
        'solution': (
            "Locate the break using a continuity tester or automated optical inspection. "
            "For thin trace breaks, apply conductive silver epoxy or solder a jumper wire "
            "across the gap. Re-inspect under magnification to confirm continuity restoration."
        )
    },
    'short': {
        'severity': 'Critical',
        'consequence': (
            "A short circuit creates an unintended low-resistance path between two nets, "
            "typically VCC and GND. This causes excessive current draw, overheating, and "
            "can permanently damage ICs, voltage regulators, or burn traces on the board."
        ),
        'solution': (
            "Identify the shorted nets using a multimeter in continuity mode before powering "
            "the board. Remove excess solder bridges using solder wick and flux. "
            "If the short is in copper pour, carefully scrape the unwanted copper with a "
            "precision knife and verify isolation with a multimeter."
        )
    },
    'spur': {
        'severity': 'Medium',
        'consequence': (
            "Spurs are unintended thin copper protrusions from a trace that can reduce "
            "clearance to adjacent traces. At high frequencies they act as antennas causing "
            "EMI issues, and under high voltage they risk dielectric breakdown and arcing."
        ),
        'solution': (
            "Remove the spur using a precision PCB router or sharp scalpel under magnification. "
            "After removal, clean the area with isopropyl alcohol and inspect the parent trace "
            "for damage. Apply conformal coating if the board operates in high-humidity environments."
        )
    },
    'spurious_copper': {
        'severity': 'High',
        'consequence': (
            "Spurious copper is unintended copper remaining after etching, which can create "
            "unintended short circuits between adjacent nets or reduce insulation resistance. "
            "On high-frequency boards it distorts impedance-controlled traces causing signal integrity issues."
        ),
        'solution': (
            "Carefully remove the spurious copper using a scalpel or micro-abrasive tool under "
            "a microscope. Verify electrical isolation with a hi-pot tester between affected nets. "
            "Review the etching process parameters to prevent recurrence in production."
        )
    }
}

def get_diagnosis(fault_class):
    return DIAGNOSTICS.get(fault_class, {
        'severity': 'Unknown',
        'consequence': 'No diagnostic data available for this fault type.',
        'solution': 'Manual inspection recommended.'
    })