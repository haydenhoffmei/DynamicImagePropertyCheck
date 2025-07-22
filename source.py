#-------------------------------------------------------------------------------
# Comparing Properties
#
# This script can be run through the command line.
#
# Hayden Hoffmeister  -  v1.5   7/8/25
#-------------------------------------------------------------------------------


# import statement
import subprocess
import json
import os
import arcgis
import arcpy
import pprint
import argparse



def mosaicProperty(mdObj):

    propertyDict = {
        "rows_maximum_imagesize":"maxRequestSizeY",
        "columns_maximum_imagesize":"maxRequestSizeX",
        "allowed_compressions":"allowedCompressionMethods",
        "default_compression_type":"defaultCompressionMethod",
        "JPEG_quality":"JPEGQuality",
        "LERC_Tolerance":"LERCTolerance",
        "resampling_type":"defaultResamplingMethod",
        "clip_to_footprints":"clipToFootprint",
        "footprints_may_contain_nodata":"footprintMayContainNoData",
        "clip_to_boundary":"clipToBoundary",
        "color_correction":"applyColorCorrection",
        "allowed_mensuration_capabilities":"allowedMensurationCapabilities",
        "default_mensuration_capabilities":"defaultMensurationCapability",
        "allowed_mosaic_methods":"allowedMosaicMethods",
        "default_mosaic_method":"defaultMosaicMethod",
        "order_field":"orderField",
        "order_base":"orderBaseValue",
        "sorting_order":"sortAscending",
        "mosaic_operator":"mosaicOperator",
        "blend_width":"blendWidth",
        "view_point_x":"viewpointSpacingX",
        "view_point_y":"viewpointSpacingY",
        "max_num_per_mosaic":"maxRastersPerMosaic",
        "cell_size_tolerance":"cellSizeToleranceFactor",
        "metadata_level":"rasterMetadataLevel",
        "use_time":"useTime",
        "start_time_field":"startTimeField",
        "end_time_field":"endTimeField",
        "time_format":"timeValueFormat",
        "geographic_transform":"GCSTransforms",
        "max_num_of_download_items":"maxDownloadImageCount",
        "max_num_of_records_returned":"maxRecordsReturned",
        "minimum_pixel_contribution":"minimumPixelContribution",
        "processing_templates":"processingTemplates",
        "default_processing_template":"defaultProcessingTemplate",
        "product_definition": "productDefinition",
        "product_band_definitions": "productBandDefinitions"
    }

    dictObj = {}
    MosaicObj = arcpy.Describe(mdObj)

    for key,value in propertyDict.items():
        try:
            if key == "resampling_type":
                dictObj[key] = getattr(MosaicObj, value).split(' ', 1 )[0].upper()
            elif key == "processing_templates":
                dictObj[key]="None"
            else:
                dictObj[key] = getattr(MosaicObj, value)
        except:
            continue

    return dictObj



def checkFieldsFunc(defaultFields,checkFields):

    for i in defaultFields:
        for j in checkFields:
            if i["name"] == j["name"]:
                if i != j:
                    print("Field mismatch\nDEFAULT FIELD:")
                    pprint.pprint(i)
                    print("CHECK FIELD:")
                    pprint.pprint(j)

    return



def checkProperties(default, check):

    try:
        defaultProps = mosaicProperty(default)
        checkProps = mosaicProperty(check)
    except:
        print("failed to MD properties")
        return

    if len(defaultProps) != len(checkProps):
        print("mismatched jsons\nDEFAULT:")
        pprint.pprint(default)
        print("CHECK:")
        pprint.pprint(check)
    else:
        for key in defaultProps:
            if key not in checkProps:
                print("missing parameter ({})".format(key))
            elif defaultProps[key] != checkProps[key]:
                value = "Property mismatch\nDEFAULT PROPERTY:   {}:{}\nCHECK PROPERTY:     {}:{}".format(key,defaultProps[key],key,checkProps[key])
                print(value)
            else:
                print("valid")

    return



def checkRestProperties():

    try:
        default = arcgis.raster.ImageryLayer(defaultUrl)
        check = arcgis.raster.ImageryLayer(checkUrl)
    except:
        print("failed to read imagery layer")
        return

    defaultDict = dict(default.properties)
    #defaultDict.pop("fields")
    defaultDict.pop("rasterFunctionInfos")

    checkDict = dict(check.properties)
    #checkDict.pop("fields")
    checkDict.pop("rasterFunctionInfos")

    for key in defaultDict:
        if key == "fields":
            defaultFields = defaultDict[key]
            checkFields = checkDict[key]
            checkFieldsFunc(defaultFields,checkFields)
        elif key not in checkDict:
            print("missing parameter ({})".format(key))
        elif defaultDict[key] != checkDict[key]:
            value = "Property mismatch\nDEFAULT PROPERTY:   {}:{}\nCHECK PROPERTY:     {}:{}".format(key,defaultDict[key],key,checkDict[key])
            print(value)

    return


def main():

    parser = argparse.ArgumentParser()
    parser.add_argument('default')#, type=str, required=True, help='')
    parser.add_argument('check')#, type=str, required=True, help='')
    parser.add_argument('type')#, type=str, choices=['rest', 'file'], required=True, help='')
    args = parser.parse_args()

    default = args.default
    check = args.check

    if args.type == 'rest':
        checkRestProperties(default, check)
    if args.type == 'file':
        checkProperties(default, check)

    pass


if __name__ == '__main__':
    main()
