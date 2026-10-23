import random

def _summary(frames, data_frames, ack_frames, piggyback_frames, data_size, ack_size):
    total_bytes = 0
    for f in frames:
        if f["type"] == "DATA":
            total_bytes += data_size
        elif f["type"] == "ACK":
            total_bytes += ack_size
        else:
            total_bytes += data_size + ack_size
    ack_bytes = ack_frames * ack_size + piggyback_frames * ack_size
    overhead = (ack_bytes / total_bytes * 100) if total_bytes else 0
    return {
        "frames": frames,
        "data_frames": data_frames,
        "ack_frames": ack_frames,
        "piggyback_frames": piggyback_frames,
        "total_frames": len(frames),
        "total_bytes": total_bytes,
        "ack_overhead_pct": overhead,
    }

def simulate(a_to_b, b_to_a, data_size=1000, ack_size=40, wait_limit_ms=100, seed=42):
    random.seed(seed)
    timeline = []
    normal = []
    piggy = []

    # Normal ACK: every received DATA gets a separate ACK.
    # Reverse-direction data is sent separately after the ACK.
    seq_a = 1
    seq_b = 1
    for i in range(max(a_to_b, b_to_a)):
        if i < a_to_b:
            normal.append({"type": "DATA", "direction": "A→B", "seq": seq_a, "ack": ""})
            timeline.append({"Step": len(timeline)+1, "Normal": f"A→B DATA {seq_a}",
                             "Piggybacking": f"A→B DATA {seq_a}"})
            seq_a += 1
            normal.append({"type": "ACK", "direction": "B→A", "seq": "", "ack": seq_a-1})
        if i < b_to_a:
            normal.append({"type": "DATA", "direction": "B→A", "seq": seq_b, "ack": ""})
            seq_b += 1

    # Piggybacking: when B has data ready, its ACK rides on B→A DATA.
    # When A has data ready, A can similarly carry the ACK for B→A DATA.
    a_remaining = list(range(1, a_to_b + 1))
    b_remaining = list(range(1, b_to_a + 1))
    a_next_ack = 0
    b_next_ack = 0
    step = 0

    while a_remaining or b_remaining:
        step += 1

        # A sends data first when available.
        if a_remaining:
            aseq = a_remaining.pop(0)
            piggy.append({"type": "DATA", "direction": "A→B", "seq": aseq, "ack": ""})
            b_next_ack = aseq

            # B has outgoing data: piggyback the ACK.
            if b_remaining:
                bseq = b_remaining.pop(0)
                piggy.append({"type": "DATA+ACK", "direction": "B→A", "seq": bseq, "ack": b_next_ack})
                b_next_ack = 0
                timeline.append({
                    "Step": len(timeline)+1,
                    "Normal": f"A→B DATA {aseq} | B→A ACK {aseq}" +
                              (f" | B→A DATA {bseq}" if bseq else ""),
                    "Piggybacking": f"A→B DATA {aseq} | B→A DATA {bseq} + ACK {aseq}"
                })
            else:
                piggy.append({"type": "ACK", "direction": "B→A", "seq": "", "ack": b_next_ack})
                b_next_ack = 0
                timeline.append({
                    "Step": len(timeline)+1,
                    "Normal": f"A→B DATA {aseq} | B→A ACK {aseq}",
                    "Piggybacking": f"A→B DATA {aseq} | B→A ACK {aseq} (timer expired/no B data)"
                })

        # If B still has data, send it. If A has an ACK pending, piggyback it.
        if b_remaining:
            bseq = b_remaining.pop(0)
            if a_remaining:
                a_next_ack = bseq
                piggy.append({"type": "DATA+ACK", "direction": "B→A", "seq": bseq, "ack": bseq})
            else:
                piggy.append({"type": "DATA", "direction": "B→A", "seq": bseq, "ack": ""})

    normal_s = _summary(normal, a_to_b + b_to_a, sum(1 for x in normal if x["type"] == "ACK"),
                        0, data_size, ack_size)
    piggy_s = _summary(piggy, a_to_b + b_to_a, sum(1 for x in piggy if x["type"] == "ACK"),
                       sum(1 for x in piggy if x["type"] == "DATA+ACK"), data_size, ack_size)

    saved = normal_s["total_frames"] - piggy_s["total_frames"]
    saved_pct = (saved / normal_s["total_frames"] * 100) if normal_s["total_frames"] else 0

    return {
        "normal": normal_s,
        "piggyback": piggy_s,
        "comparison": {
            "frames_saved": saved,
            "bandwidth_saved_pct": saved_pct
        },
        "timeline": timeline,
        "parameters": {
            "a_to_b": a_to_b,
            "b_to_a": b_to_a,
            "data_size": data_size,
            "ack_size": ack_size,
            "wait_limit_ms": wait_limit_ms,
            "seed": seed,
        }
    }
        "ack_overhead_pct": piggy_ack_overhead,
    }

    return {
        "normal": normal_s,
        "piggyback": piggy_s,
        "comparison": {
            "frames_saved": frames_saved,
            "bandwidth_saved_pct": transmission_reduction_pct,
            "transmission_reduction_pct": transmission_reduction_pct,
            "efficiency_pct": efficiency_pct,
        },
        "timeline": timeline,
        "parameters": {
            "num_frames": N,
            "data_size": data_size,
            "ack_size": ack_size,
            "a_to_b": N,
            "b_to_a": N,
        }
    }
