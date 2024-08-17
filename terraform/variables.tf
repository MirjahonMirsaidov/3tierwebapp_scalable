variable "db" {
  type    = object({
    username = string
    password = string
    name = string
  })
}