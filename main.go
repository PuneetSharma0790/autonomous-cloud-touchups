package main

// resource management in a cloud env simple demo

import (
	"fmt"
	"math/rand"
	"time"
)

type Resource struct {
	ID   string
	Type string
	Used bool
}

type Cloud struct {
	Resources []Resource
}

func (c *Cloud) ProvisionResource(resourceType string) Resource {
	id := fmt.Sprintf("res-%d", rand.Intn(1000))
	resource := Resource{ID: id, Type: resourceType, Used: false}
	c.Resources = append(c.Resources, resource)
	return resource
}

func (c *Cloud) AllocateResource() *Resource {
	for i := range c.Resources {
		if !c.Resources[i].Used {
			c.Resources[i].Used = true
			return &c.Resources[i]
		}
	}
	return nil
}

func (c *Cloud) DeallocateResource(id string) {
	for i := range c.Resources {
		if c.Resources[i].ID == id {
			c.Resources[i].Used = false
			break
		}
	}
}

func main() {
	rand.Seed(time.Now().UnixNano())
	cloud := Cloud{}

	for i := 0; i < 5; i++ {
		cloud.ProvisionResource("VM")
	}

	resource := cloud.AllocateResource()
	if resource != nil {
		fmt.Printf("Allocated Resource: %s\n", resource.ID)
	}

	cloud.DeallocateResource(resource.ID)
	fmt.Println("Deallocated Resource:", resource.ID)
}
