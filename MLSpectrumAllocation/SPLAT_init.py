import os
import urllib.request
import zipfile
import shutil
import glob
import subprocess
from Commons.Point import GeographicPoint, to_geographic, Point

SDF_DIR = 'rsc/splat/sdf'


def create_lrp_file():
    LRP = "25.000  ;   Earth Dielectric Constant (Relative permittivity)\n" + \
          "0.020   ;   Earth Conductivity (Siemens per meter)           \n" + \
          "301.000 ;   Atmospheric Bending Constant (N-units)           \n" + \
          "600.000 ;   Frequency in MHz (20 MHz to 20 GHz)              \n" + \
          "5       ;   Radio Climate (5 = Continental Temperate)        \n" + \
          "1       ;   Polarization (0 = Horizontal, 1 = Vertical)      \n" + \
          "0.50    ;   Fraction of situations (50% of locations)        \n" + \
          "0.90    ;   Fraction of time (90% of the time)\n"
    if not os.path.exists(SDF_DIR):
        os.makedirs(SDF_DIR)
    with open(SDF_DIR + '/splat.lrp', 'w') as fq:
        fq.write(str(LRP))


def generate_sdf_files(upper_left_loc: GeographicPoint, field_length):  # downloading and creating sdf(terrain)
    if not os.path.exists(SDF_DIR):
        os.makedirs(SDF_DIR)
    tmp_dir = SDF_DIR + '/tmp'
    if not os.path.exists(tmp_dir):
        os.makedirs(tmp_dir)

    lat_set = set(list(range(int(upper_left_loc.lat),
                             int(to_geographic(upper_left_loc, Point((0, field_length))).lat)+1)))
    lon_set = set(list(range(int(upper_left_loc.lon),
                             int(to_geographic(upper_left_loc, Point((field_length, 0))).lon)+1)))

    for lat in lat_set:
        for lon in lon_set:
            lat_str, lon_str = str(lat), str(lon + 1)
            if len(lon_str) < 3:
                lon_str = '0' + lon_str
            sdf_file = "N" + lat_str + "W" + lon_str + ".hgt.zip"
            print("Downloading Terrain file: ", sdf_file)
            terrain_file_url = "https://dds.cr.usgs.gov/srtm/version2_1/SRTM3/North_America/" + sdf_file
            try:
                with urllib.request.urlopen(terrain_file_url) as response, open(
                        tmp_dir + '/' + str(sdf_file), 'wb') as f:
                    shutil.copyfileobj(response, f)
            except IOError as e:
                raise ("Error: terrain file " + sdf_file + " NOT found!", e)
            print('Unzipping SDF file', sdf_file)
            try:
                # ---uncompress the zip file-----------------#
                zip_ref = zipfile.ZipFile(tmp_dir + "/" + str(sdf_file), 'r')
                zip_ref.extractall(tmp_dir)
                zip_ref.close()
            except (zipfile.BadZipFile, zipfile.LargeZipFile) as e:
                raise ("Error: Unzipping for", sdf_file, ' was NOT successful!', e)
    print("Downloading and unzipping was successful.")

    # convert zip file to hgt_file using strm2sdf command line
    owd = os.getcwd()
    os.chdir(SDF_DIR)
    pp = os.getcwd()
    try:
        for hgt_file in glob.glob('./tmp/*.hgt'):
            subprocess.call(["srtm2sdf", hgt_file])
            # subprocess.call(["srtm2sdf-hd", hgt_file])
    except (ValueError, subprocess.CalledProcessError, OSError) as e:
        # e = sys.exc_info()[0]
        raise ("Error: converting .hgt file\n", e, "was NOT successful!")
    finally:
        os.chdir(owd)
        shutil.rmtree(tmp_dir)  # remove the temporary directory created at the beginning


if __name__ == "__main__":
    generate_sdf_files(GeographicPoint(40.800595, 73.107507), 10000)
    create_lrp_file()
