# prepare the copied src directory 
python process_markdowns.py

# copy pandoc_script into the temp src_copy directory 
cp pandoc_script.py header.tex cover.tex listings_setup.tex src_copy

# run pandoc_script from src_copy directory 
cd src_copy
python pandoc_script.py
mv bids.pdf ..
cd ..

# rm -rf src_copy