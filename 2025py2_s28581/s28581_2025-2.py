from Bio import Entrez, SeqIO
import pandas as pd, matplotlib.pyplot as plt, time

class NCBI:
    def __init__(s, email, key): Entrez.email, Entrez.api_key, s.r = email, key, []
    def search(s, taxid):
        r = Entrez.read(Entrez.esearch(db="nucleotide", term=f"txid{taxid}[Organism:exp]", usehistory="y", retmax=0))
        s.qk, s.wenv, s.cnt = r["QueryKey"], r["WebEnv"], int(r["Count"])
        return s.cnt
    def fetch(s, minlen, maxlen, maxrec=200):
        for i in range(0, min(s.cnt, maxrec), 100):
            h = Entrez.efetch(db="nucleotide", rettype="gb", retmode="text", retstart=i, retmax=100, webenv=s.wenv, query_key=s.qk)
            for r in SeqIO.parse(h, "genbank"):
                l = len(r.seq)
                if minlen <= l <= maxlen: s.r.append({"accession": r.id, "length": l, "description": r.description})
            h.close(); time.sleep(0.34)
    def save_csv(s, f): pd.DataFrame(s.r).sort_values("length", ascending=False).to_csv(f, index=False); print(f"[+] CSV: {f}")
    def plot(s, f):
        df = pd.DataFrame(s.r).sort_values("length", ascending=False)
        plt.figure(figsize=(10,6)); plt.plot(df["accession"], df["length"], "o-"); plt.xticks(rotation=90, fontsize=6)
        plt.xlabel("Accession"); plt.ylabel("Length"); plt.title("Sequence Lengths"); plt.tight_layout(); plt.savefig(f); plt.close()
        print(f"[+] PNG: {f}")

if __name__ == "__main__":
    e, k = input("Email: "), input("API Key: ")
    t, minl, maxl, maxr = input("TaxID: "), int(input("Min len: ")), int(input("Max len: ")), int(input("Max records: "))
    n = NCBI(e, k)
    if n.search(t): n.fetch(minl, maxl, maxr); n.save_csv(f"taxid_{t}.csv"); n.plot(f"taxid_{t}.png")
