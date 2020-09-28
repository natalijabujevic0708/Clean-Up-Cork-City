# Database structure

Creating the database structure was the first step in the development. There are 5 collections in the database:

## **active_locations** collection:
 
 There are two types of documents:
 1. Locations that **are not yet cleaned**:


```txt
{
  "_id" :                  <ObjectID>,
  "status":                <string>,
  "address_of_location":   <string>,
  "picture_name":          <string>,
  "uploaded_by":           <string>,
  "date":                  <string>,
  "latitude_of_location":  <double>,
  "longitude_of_location": <double>,
}
```
Example:
```txt
{
    "_id": ObjectId("5f6e0401a87c084c5d9d7eab"),
    "status": "not_cleaned",
    "address_of_location":"23 Sunday's Well Road, Sunday's Well,    
	Cork, Ireland",
    "picture_name":"dundrum-luas-stop-rubbish.jpg",
	"uploaded_by":"Natalija",
    "date":"2020-09-25 15:51:45",
    "latitude_of_location": 51.8994527,
    "longitude_of_location":-8.4910679
}
```

2. Locations that **are cleaned**:

```txt
{
  "_id" :                  <ObjectID>,
  "status":                <string>,
  "address_of_location":   <string>,
  "picture_name":          <string>,
  "cleaned_picture_name"   <string>,
  "uploaded_by":           <string>,
  "date_of_cleanup":       <string>,
  "number_of_people":      <string>,
  "latitude_of_location":  <double>,
  "longitude_of_location": <double>,
}
```
Example:
```txt
{
	"_id":ObjectId("5f6e10ee88f81ea02521484a"),
	"status":"cleaned",
	"address_of_location":"Lough Park, The Lough, Cork, Ireland",
	"picture_name":"1311dutch17be.jpg",
	"cleaned_picture_name":"1311dutch17af.jpg",
	"uploaded_by":"Natalija",
	"date_of_cleanup":"2020-09-05",
	"number_of_people":"5",
	"latitude_of_location": 51.8889665,
	"longitude_of_location":-8.4842456"
	
}
```
## **deleted_locations** collection:


```txt
{
  "_id":                  <ObjectID>,
  "address":              <string>,
  "reason_for_deleting":  <string>,
  "deleted_by":           <string>,
  "date":                 <string>

}
```
Example:
```txt
{
	"_id":ObjectId("5f6e03a0a87c084c5d9d7ea8"),
	"address":"Old Youghal Road, Cork, Ireland",
	"reason_for_deleting":"wrong address",
	"deleted_by":"Natalija",
	"date":"2020-09-25 16:50:11"
}
```
## **fs.chunks** collection:

```txt
{
  "_id":                  <ObjectID>,
  "files_id":             <ObjectID>,
  "n":                    <Integer>,
  "data":                 <Binary Data>
}
```
Example:
```txt
{
	"_id":ObjectId("5f39835fa87c68e6369ee3c6"),
	"files_id":ObjectId("5f39835ea87c68e6369ee3c5"),
	"n": 0,

	"data":Binary('/9j/4AAQSkZJRgABAQEAYABgAAD 2wBDAAQCAwMDAgQDAwMEBAQEBQkGBQUFBQsICAYJDQsNDQ0LDAwOEBQRDg8TDwwM hgSExUW...', 0)
}
```
## **fs.files** collection:

```txt
{
  "_id":                  <ObjectID>,
  "filename":             <string>,
  "contentType":          <string>,
  "md5":                  <string>,
  "chunkSize":            <Integer>,
  "length":               <Integer>
  "uploadDate":           <date>
}
```
Example:
```txt
{ 
	"_id":ObjectId("5f39835ea87c68e6369ee3c5"),
	"filename":"Garbage,_Sheppards_Bush___Super_Portrait.jpg",
	"contentType":"image/jpeg",
	"md5":"d4a2b1c57a7f76c19eef7596adc59b91",
	"chunkSize": 261120,
	"length":136518,
	"uploadDate": 2020-08-16T19:05:04.243+00:00
}
```

## **users** collection:


```txt
{
  "_id":                  <ObjectID>,
  "name":                 <string>,
  "email":                <string>,
  "password":             <string>,
  "home_address":         <string>,
  "date_of_birth":        <string>

}
```
Example:
```txt
{
	"_id":ObjectId("5f6e02873c28610dc48b82c7"),
	"name":"Natalija",
	"email":"natalija@gmail.com",
	"password":"hrwspciuugtdxc",
	"home_address":"7/8 Shandon Street",
	"date_of_birth":"1990-08-07"
}	
```
