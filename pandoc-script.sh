# make a copy of src directory
rm -rf copy_src
rm bids-specs.pdf
mkdir copy_src
cp -a ./src/* ./copy_src
cd copy_src
pwd

# rename files within the copy_src directory
for j in *.md; do
    if [ ${j:0:1} -eq '0' ]; then
        mv "$j" "${j//${j:1:1}/${j:1:1}0}"
    fi
done

# renaming and copying files in the 04-modality-specific-files directory
cd ./04-modality-specific-files
# pwd
cp -a ./images/* ../images;

for i in ./*.md; do
    mv "$i" "${i//[0]/04}"
done

cp -a ./*.md ..;

# doing same as above for the appendices directory
cd ../99-appendices
# pwd

# renaming files in the appendices directory
for k in ./*.md; do
    mv "$k" "${k//[0]/99}"
done

cp -a ./*.md ..;
cd ..
pandoc index.md *.md -f markdown_github --include-before-body cover.tex  --toc --listings -H listings_setup.tex -H header.tex --include-in-header chapter_break.tex -V toc-title='Table of Contents' -V linkcolor:blue -V geometry:a4paper -V geometry:margin=2cm --pdf-engine=xelatex  -o bids-specs.pdf

cp bids-specs.pdf ..
cd ..
rm -rf copy_src
open bids-specs.pdf
