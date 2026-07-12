import streamlit as st
import numpy as np
from datetime import date
import base64

# identification
import log

#qrcode
from PIL import Image, ImageOps
from pyzbar.pyzbar import decode
import qrcode

#license
import json

#security
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.asymmetric import padding
from cryptography.hazmat.primitives import hashes

log.logging()

st.image("img/Zero white title.png", width="stretch")

"# Zero licenses"
st.caption("GENERATE A NEW LICENSE", text_alignment="center")

#licenses param
st.caption(":material/person: Geologist", text_alignment="center")
c = st.columns(2)
fname = c[0].text_input(":material/person: First name", "")
name = c[1].text_input(":material/person: Name", "")
cie = st.text_input(":material/person: Company", "")
  
st.caption(":material/license: License", text_alignment="center")
c = st.columns(2)
license_type = c[0].selectbox(":material/license: License type", ["PC","server"])
license_cover = c[1].selectbox(":material/license: License cover", ["Trial","Premium"])
expiry = st.date_input(":material/license: Expiry", "today", format="YYYY-MM-DD")

# machine id
st.caption(":material/computer: Machine identification", text_alignment="center")
qr_source = st.radio(":material/computer: Machine ID source", ["Text", "Image file", "Camera"], horizontal=True)
machine_id = None


# def read_qr(image):
#   decoded = decode(image)
#   if decoded:
#     return decoded[0].data.decode("utf-8")
#   return None


def read_qr(image: Image.Image):
  """Try hard to decode a QR code from a possibly messy camera photo."""
  base = image.convert("L")  # grayscale

  candidates = []

  # a few preprocessing variants, cheap to generate
  for scale in (1.0, 0.5, 1.5, 2.0):
    img = base
    if scale != 1.0:
      w, h = base.size
      img = base.resize((int(w * scale), int(h * scale)))
    img = ImageOps.autocontrast(img)
    candidates.append(img)
  
  for base_img in list(candidates):
    for angle in (90, 180, 270):
      candidates.append(base_img.rotate(angle, expand=True))
  
  for cand in candidates:
    decoded = decode(cand.convert("RGB"))
    if decoded:
      return decoded[0].data.decode("utf-8")

  return None


if qr_source == "Camera":
  camera = st.camera_input(":material/computer: Scan machine QR code")
  if camera:
    img = Image.open(camera).convert("RGB")
    machine_id = read_qr(img)


    if machine_id:
      st.success("Machine ID detected")
      st.code(machine_id)
        
    else:
      st.error("QR code not recognized")


elif qr_source == "Image file":
  qr_file = st.file_uploader( ":material/computer: Upload machine QR code", type=["png", "jpg", "jpeg"])
  if qr_file:
    img = Image.open(qr_file).convert("RGB")
    machine_id = read_qr(img)    
    if machine_id:
      st.success("Machine ID detected")
      st.code(machine_id)
    else:
      st.error("QR code not recognized")

else :
  machine_id = st.text_input(":material/computer: Machine ID", "").strip()

st.caption(":material/security: Private key", text_alignment="center")
key_file = st.file_uploader(":material/security: Encrypted private key", type=["pem"])
password = st.text_input("Private key password",type="password")

hcont = st.container(horizontal_alignment="center")
if hcont.button(":material/license: Generate license", type="secondary") :
  if not machine_id:
    st.error("Missing machine ID")
    st.stop()

  if not key_file:
    st.error("Missing private key")
    st.stop()


  try:
    private_key = serialization.load_pem_private_key( key_file.read(), password=password.encode())

    license_data = {
            "geologist_fname": fname, "geologist_name": name, "geologist_cie": cie, "machine_id": machine_id,
            "expires": str(expiry), "license_type": license_type, "license_cover": license_cover, }

    # message = json.dumps( license_data, sort_keys=True ).encode()
    message = json.dumps(license_data, sort_keys=True, separators=(",", ":")).encode()

    signature = private_key.sign(
            message,
            padding.PSS(
                mgf=padding.MGF1(hashes.SHA256()),
                salt_length=padding.PSS.MAX_LENGTH
            ),
            hashes.SHA256()
        )

    # license_file = {
    #   "data": license_data,
    #   "signature": signature.hex(),
    # }

    license_file = {
      "data": license_data,
      "signature": base64.b64encode(signature).decode("ascii"),
    }
    
    st.toast(":material/license: License generated")

    lic_name = f"zero_license-{license_type}_{fname}_{name}_{expiry}.json"

    hcont.download_button(
        ":material/download: Download license",
        json.dumps(license_file, indent=4),
        file_name=lic_name,
        mime="application/json",
        type="primary",
    )  
  except Exception as e:
    st.error(f"License generation failed: {e}")
