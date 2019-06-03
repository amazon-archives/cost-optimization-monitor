#!/bin/bash
#
# This assumes all of the OS-level configuration has been completed and git repo has already been cloned
#
# This script should be run from the repo's deployment directory
# cd deployment
# ./build-s3-dist.sh source-bucket-base-name version-code
#
# Parameters:
#  - source-bucket-base-name: Name for the S3 bucket location where the template will source the Lambda
#    code from. The template will append '-[region_name]' to this bucket name.
#    For example: ./build-s3-dist.sh solutions v1.1.0
#    The template will then expect the source code to be located in the solutions-[region_name] bucket
#
#  - version-code: version of the package

# Check to see if input has been provided:
if [[ -z "$1" ]] || [[ -z "$2" ]]; then
    echo "Please provide the base source bucket name and version where the lambda code will eventually reside."
    echo "For example: ./build-s3-dist.sh solutions v1.1.0"
    exit 1
fi

# Get reference for all important folders
template_dir="$PWD"
dist_dir="$template_dir/dist"
source_dir="$template_dir/../source"

echo "------------------------------------------------------------------------------"
echo "[Init] Clean old dist and es_tools.egg-info folders"
echo "------------------------------------------------------------------------------"
echo "rm -rf $dist_dir"
rm -rf "$dist_dir"
echo "find $source_dir -iname \"es_tools.egg-info\" -type d -exec rm -r \"{}\" \; 2> /dev/null"
find "$source_dir" -iname "es_tools.egg-info" -type d -exec rm -r "{}" \; 2> /dev/null
echo "find $source_dir -iname \"dist\" -type d -exec rm -r \"{}\" \; 2> /dev/null"
find "$source_dir" -iname "dist" -type d -exec rm -r "{}" \; 2> /dev/null
echo "find ../ -type f -name '.DS_Store' -delete"
find "$source_dir" -type f -name '.DS_Store' -delete
echo "mkdir -p $dist_dir"
mkdir -p "$dist_dir"

echo "------------------------------------------------------------------------------"
echo "[Packing] Templates"
echo "------------------------------------------------------------------------------"
echo "cp -f $template_dir/cost-optimization-monitor.template dist"
cp -f "$template_dir/cost-optimization-monitor.template" "$dist_dir"

echo "Updating code source bucket in template with $1"
replace="s/%%TEMPLATE_BUCKET_NAME%%/$1/g"
echo "sed -i '' -e $replace $dist_dir/cost-optimization-monitor.template"
sed -i '' -e "$replace" "$dist_dir"/cost-optimization-monitor.template

echo "Updating code source version in template with $2"
replace="s/%%VERSION%%/$2/g"
echo "sed -i '' -e $replace $dist_dir/cost-optimization-monitor.template"
sed -i '' -e "$replace" "$dist_dir"/cost-optimization-monitor.template

echo "Updating dist bucket in template with $3"
replace="s/%%DIST_BUCKET_NAME%%/$3/g"
echo "sed -i '' -e $replace $dist_dir/cost-optimization-monitor.template"
sed -i '' -e "$replace" "$dist_dir"/cost-optimization-monitor.template

echo "------------------------------------------------------------------------------"
echo "[Packing] ES Tools"
echo "------------------------------------------------------------------------------"
cd "$source_dir"/es_tools || exit 1
python setup.py sdist
cp "$source_dir"/es_tools/dist/*.gz "$dist_dir"/
cp "$source_dir"/es_tools/export.json "$dist_dir"/

echo "Updating code source version in dashboard description with $2"
replace="s/%%VERSION%%/$2/g"
echo "sed -i '' -e $replace $dist_dir/export.json"
sed -i '' -e "$replace" "$dist_dir"/export.json

echo "------------------------------------------------------------------------------"
echo "[Packing] Helper"
echo "------------------------------------------------------------------------------"
cd "$source_dir"/helper || exit 1
zip -q -r9 "$dist_dir"/helper.zip ./*

