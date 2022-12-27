#the working directory
setwd('your\\directory')


simple_indexer = function(file_name, type_desired) {

  #the file you want to index info from
  #omitting NA
  #data from: https://github.com/KeithGalli/pandas
  file = na.omit(read.csv(file_name))
  
  #checking what the structure is like
  head(file)
  
  
  #indexing pokemon by type
  type_search = type_desired
  
  type1 = which(tolower(file[, 3]) == type_search)
  type2 = which(tolower(file[, 4]) == type_search)
  type_final = sort(c(type1, type2))
  
  #printing total of the type
  print(paste('there are', length(type_final), type_search, 'types'))
  
  #printing the names of the pokemon
  pokemon_names = file[type_final, 2]
  #pokemon_names
  
  
  #checking which are legendary pokemon
  is_legendary = NULL
  
  #if there are legendaries of that type they are displayed
  #otherwise it is stated that there are none of that type
  if (length(which(file[type_final, 12] == T) >= 1)) {
    is_legendary = which(file[type_final, 12] == T)
    print('these are the legendary pokemon of that type:')
    file[type_final[is_legendary], 2]
  } else {
    print('there are no legendaries of that type')
  }
}