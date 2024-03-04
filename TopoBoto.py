#import modules
import boto3
import arcpy
import sys
import os
from botocore.client import Config
from botocore import UNSIGNED
def download():
#create aws credentials even though s3 is public
    cred = {"aws_access_key_id": "", 
                "aws_secret_access_key": "", 
                "config": Config(signature_version=UNSIGNED)}
    #create session
    session = boto3.Session()
    client = session.client('s3', **cred)
    #define bucket name and object key/prefix
    bucket = 'noaa-ocs-nationalbathymetry-pds'
    prefix = 'BlueTopo/_BlueTopo_Tile_Scheme/BlueTopo_Tile_Scheme'
    #use pagenitor to iterate through objects-objs (from github repo)
    pageinator = client.get_paginator("list_objects_v2")
    objs = pageinator.paginate(Bucket=bucket, Prefix=prefix).build_full_result()
    if len(objs) == 0:
        print(f"No geometry found in {prefix}")
       # return None
    #source name variable. 0 index to identify the desired geopackage within the objs. Key identifies key for geopackage   
    source_name = objs["Contents"][0]["Key"]
    #set output file name as variable to scratch folder. 
    output_f = arcpy.env.scratchFolder
    #set output data set name, using output_f variable, and output_ds name as Output.gpkg
    output_ds = os.path.join(output_f, "Output.gpkg")
    #download object. Clarify bucket, source name (gpkg), and the output dataset name(Output.gpkg)
    client.download_file(bucket, source_name, output_ds)
    #overwrite output_ds content when running code again.
    arcpy.env.overwriteOutput = True
    #set arcpy workspace to where geopackage/output_ds is located
    arcpy.env.workspace = output_ds
    #input feature for conversion variable. naming convetion. split "name" and extension. 
    inFeatures = [f"main.{os.path.splitext(os.path.basename(source_name))[0]}"]
    #Convert the inuput (gpkg) to a shapefile (.shp) output
    arcpy.FeatureClassToShapefile_conversion(inFeatures, output_f) 
    print(output_f)   
    return None

#run main script-run download function
if __name__=="__main__":
    download()
    















