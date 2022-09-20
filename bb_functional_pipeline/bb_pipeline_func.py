#!/bin/env python
#
# Script name: bb_pipeline_func.py
#
# Description: Script with the functional pipeline.
# 			   This script will call the rest of functional functions.
#
# Authors: Fidel Alfaro-Almagro, Stephen M. Smith & Mark Jenkinson
#
# Copyright 2017 University of Oxford
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#    http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#

import os.path
import sys
import json

sys.path.insert(1, os.path.dirname(__file__) + "/..")
import bb_pipeline_tools.bb_logging_tool as LT


def bb_pipeline_func(subject, fileConfiguration):

    # building blocks for more elaborate, generic design.fsf matching system
    # store old file paths in subject's fMRI directory

    subjDir = f"{os.getcwd()}/{subject}"

    f = open(subjDir + "/filenames.txt", "w")
    for k in fileConfiguration.keys():
        if "oldpath" in k:
            f.write(f"{k}:{fileConfiguration[k]}\n")
    f.close()

    logger = LT.initLogging(__file__, subject)
    logDir = logger.logDir
    baseDir = logDir[0 : logDir.rfind("/logs/")]

    jobsToWaitFor = ""

    subname = subject.replace("/", "_")

    # st = (
    #     # '${FSLDIR}/bin/fsl_sub -T 5 -N "bb_postprocess_struct_'
    #     '${FSLDIR}/bin/fsl_sub -q ${QUEUE_STANDARD} -N "bb_postprocess_struct_'
    #     + subname
    #     + '" -l '
    #     + logDir
    #     + " -j "
    #     + str(jobHold)
    #     + "$BB_BIN_DIR/bb_functional_pipeline/bb_postprocess_struct "
    #     + subject
    # )

    rfMRI_nums = [
         k.split("_")[-1]
         for k in fileConfiguration.keys()
         if "rfMRI" in k and "oldpath" not in k and "SBRef" not in k
    ]

    # print(st)

    print("Beginning functional pipeline")

    print("Running bb_postprocess_struct...")
#    jobPOSTPROCESS = LT.runCommand(
#        logger,
#        "$BB_BIN_DIR/bb_functional_pipeline/bb_postprocess_struct "
#        + subject,
#        "bb_postprocess_struct_"
#        + subname
#    )
#    print("bb_postprocess_struct completed.")

#    print("Running tvb_prepare_gradEchoFieldMap...") # KEEP THIS SECTION COMMENTED OUT SF 22.08.2022
#    jobGEFIELDMAP = LT.runCommand(
#        logger,
#        "$BB_BIN_DIR/bb_functional_pipeline/tvb_prepare_gradEchoFieldMap "
#        + subject,
#        "tvb_prepare_gradEchoFieldMap_"
#        + subname
#    )
#    print("tvb_prepare_gradEchoFieldMap completed.")
    # if ("rfMRI" in fileConfiguration) and (fileConfiguration["rfMRI"] != ""):

    jobCLEAN_LAST_rfMRI = "-1"

    if len(rfMRI_nums) > 0:
        print("rfMRI files found. Running rfMRI subpipe")
        for i in range(len(rfMRI_nums)):
            # if it's the first rfMRI file start upon completion of fieldmap
            # otherwise use clean job ID from previous rfMRI iteration

#            print(f"Running rfMRI_{i} prep...")
#            jobPREPARE_R = LT.runCommand(
#                logger,
#                "$BB_BIN_DIR/bb_functional_pipeline/bb_prepare_rfMRI "
#                + subject
#                + f" {rfMRI_nums[i]}",
#                f"bb_prepare_rfMRI_{i}_"
#                + subname
#            )
            # TODO: Embed the checking of the fieldmap inside the independent steps -- Every step should check if the previous one has ended.
            #print(f"FILE CONFIG IN FUNC: {fileConfiguration}")
            #if ("rfMRI" in fileConfiguration) and (fileConfiguration["rfMRI"] != ""):

#            print(f"rfMRI_{i} prep completed.")

#            print("Running FEAT...")
#            jobFEAT_R = LT.runCommand(
#                logger,
#                "feat "
#                + baseDir
#                #
#                # + f"/fMRI/rfMRI_{i}.fsf " + subject,
#                + f"/fMRI/rfMRI_{i}.fsf",
#                f"bb_feat_rfMRI_{i}_ns_"
#                + subname
#           )
#            print("FEAT completed.")

            print(f"Running rfMRI_{i} FIX...")
            training_file = 0 # This next piece toggles between the training files
            if rfMRI_nums[i] == 0:
                training_file = "musebid_rest_Training.RData"
                jobFIX = LT.runCommand(
                    logger,
                    "$BB_BIN_DIR/bb_functional_pipeline/bb_fix "
                    + subject
                    + f" {rfMRI_nums[i]} "
                    + training_file,
                    f"bb_fix_{i}_"
                    + subname
            elif rfMRI_nums[i] == 1:
                training_file = "musebid_music_Training.RData"
                jobFIX = LT.runCommand(
                    logger,
                    "$BB_BIN_DIR/bb_functional_pipeline/bb_fix "
                    + subject
                    + f" {rfMRI_nums[i]} "
		    + training_file,
                    f"bb_fix_{i}_"
                    + subname
            )
            print("FIX completed.")
            print("Running FC...")
            ### compute FC using parcellation
            jobFC = LT.runCommand(
                logger,
                "$BB_BIN_DIR/bb_functional_pipeline/tvb_FC "
                + subject
                + f" {rfMRI_nums[i]}",
                f"tvb_FC_{i}_"
                + subname
            )
            print("FC completed.")
            ### don't generate group-ICA RSNs
            # jobDR = LT.runCommand(
            # logger,
            ##'${FSLDIR}/bin/fsl_sub -T 120  -N "bb_ICA_dr_'
            #'${FSLDIR}/bin/fsl_sub -q ${QUEUE_MORE_MEM}  -N "bb_ICA_dr_'
            # + subname
            # + '"  -l '
            # + logDir
            # + " -j "
            # + jobFIX
            # + " $BB_BIN_DIR/bb_functional_pipeline/bb_ICA_dual_regression "
            # + subject,
            # )
            jobCLEAN = LT.runCommand(
                logger,
                "$BB_BIN_DIR/bb_functional_pipeline/bb_clean_fix_logs "
                + subject
                + f" {rfMRI_nums[i]}",
                f"bb_rfMRI_{i}_clean_"
                + subname
            )
            print("Cleaning up rfMRI files...")

            jobCLEAN_LAST_rfMRI = jobCLEAN
            jobsToWaitFor += f"{jobCLEAN},"
            print("Done.")
        print("rfMRI subpipe complete.")

    else:
        logger.error(
            "There is no rFMRI info. Thus, the Resting State part will not be run"
        )

    # if jobsToWaitFor != "":
    #     jobsToWaitFor += ","
    tfMRI_nums = [
        k.split("_")[-1]
        for k in fileConfiguration.keys()
        if "tfMRI" in k and "SBRef" not in k and "oldpath" not in k
    ]

    jobFEAT_LAST = "-1"

    # print(f"tfMRI_nums: {tfMRI_nums}")
    # if ("rfMRI" in fileConfiguration) and (fileConfiguration["rfMRI"] != ""):
    if len(tfMRI_nums) > 0:
        print("tfMRI files found. Running tfMRI subpipe")
        for i in range(len(tfMRI_nums)):
            # if ("tfMRI" in fileConfiguration) and (fileConfiguration["tfMRI"] != ""):

            print(f"Running tfMRI_{i} prep...")
            jobPREPARE_T = LT.runCommand(
                logger,
                " $BB_BIN_DIR/bb_functional_pipeline/bb_prepare_tfMRI "
                + subject
                + f" {tfMRI_nums[i]}",
                f"bb_prepare_tfMRI_{i}_"
                + subname
            )
            print(f"tfMRI_{i} prep complete.")

            print(f"Running FEAT on tfMRI_{i}...")
            jobFEAT_T = LT.runCommand(
                logger,
                " feat  "
                + baseDir
                + f"/fMRI/tfMRI_{i}.fsf",
                f"bb_feat_tfMRI_{i}_"
                + subname
            )
            print("FEAT completed.")

            jobFEAT_LAST = jobFEAT_T

            if jobsToWaitFor != "":
                # jobsToWaitFor = jobsToWaitFor + "," + jobFEAT_T
                jobsToWaitFor += jobFEAT_T
            else:
                jobsToWaitFor = jobFEAT_T

        print("tfMRI subpipe complete.")

    else:
        logger.error(
            "There is no tFMRI info. Thus, the Task Functional part will not be run"
        )

    if jobsToWaitFor == "":
        jobsToWaitFor = "-1"

    print("Functional pipeline complete.")

    os.rename(subjDir + "/filenames.txt", subjDir + "/fMRI/filenames.txt")
    return jobsToWaitFor


if __name__ == "__main__":
    # grab subject name from command
    subject = sys.argv[1]
    fd_fileName = "logs/file_descriptor.json"

    # check if subject directory exists
    if not os.path.isdir(subject):
        print(f"{subject} is not a valid directory. Exiting")
        sys.exit(1)
    # attempt to open the JSON file
    try:
        json_path = os.path.abspath(f"./{subject}/{fd_fileName}")
        with open(json_path, "r") as f:
            fileConfig = json.load(f)
    except:
        print(f"{json_path} could not be loaded. Exiting")
        sys.exit(1)
    # call pipeline
    bb_pipeline_func(subject, fileConfig)

