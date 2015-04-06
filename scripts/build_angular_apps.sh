# For building angular lectut static files
echo "Building lectut angular app"
cd angular_apps/lectut
grunt build
cd ../../

# For building angular yaadein static files
echo "Building yaadein angular app"
cd angular_apps/yaadein
grunt build
cd ../../
