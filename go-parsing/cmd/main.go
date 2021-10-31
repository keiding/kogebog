package main

import (
	"bytes"
	"fmt"
	"os"
	"regexp"
	"strings"
	"time"

	"github.com/morsby/mdast"
)

func main() {
	f, err := os.Open("kokkennoter.md")
	if err != nil {
		panic(err)
	}
	defer f.Close()
	doc := mdast.Parse(f)

	el := &doc
	// Total TOC
	for {
		for i := 0; i < el.Level; i++ {
			fmt.Printf("-  ")
		}
		fmt.Printf("%s\n", strings.TrimSpace(el.Title))
		el = mdast.Next(el, nil)

		if el == nil {
			break
		}
	}

	// Generate separate files
	for i, h1 := range doc.Children {
		path := "split/" + h1.Slug + "/"
		os.MkdirAll(path, 0755)
		os.WriteFile(path+"_index.md", genMd(h1, i, false), 0644)
		for j, h2 := range h1.Children {
			os.WriteFile(path+h2.Slug+".md", genMd(h2, j, true), 0644)
		}
	}
}

func genMd(sect *mdast.Section, index int, includeChildren bool) []byte {
	text := []byte(sect.Text)
	metadata := fmt.Sprintf(`
---
title: %s
weight: %d
draft: false
date: %s
`, sect.Title, (index+1)*5, time.Now())

	// if noOfServings
	noOfServings := ""
	regexServings := regexp.MustCompile(`\*Til (\d+-?\d*) persone?r?\*`)
	matches := regexServings.FindSubmatchIndex(text)
	if len(matches) == 4 {
		noOfServings = string(text[matches[2]:matches[3]])
		metadata += "noOfServings: " + noOfServings + "\n"
		text = append(text[:matches[0]], text[matches[1]:]...)

	}

	// ingredients
	indexIngredients := bytes.Index(text, []byte("**Ingredienser**"))
	indexOpskrift := bytes.Index(text, []byte("**Opskrift**"))
	if indexIngredients > -1 && indexOpskrift > -1 {
		ingredients := text[indexIngredients+len("**Ingredienser**") : indexOpskrift]
		ingredients = bytes.ReplaceAll(bytes.TrimSpace(ingredients), []byte("\n\n"), []byte("\n  - "))
		ingredients = bytes.ReplaceAll(ingredients, []byte("  - \n"), nil)
		ingredients = bytes.ReplaceAll(ingredients, []byte("*"), nil)
		metadata += "ingredients:\n  - " + string(ingredients) + "\n"

		text = text[indexOpskrift+len("**Opskrift**"):]
	}
	metadata += "---" // end of YAML front matter

	md := fmt.Sprintf("%s\n\n%s", strings.TrimSpace(metadata), text)

	if includeChildren && len(sect.Children) > 0 {
		p := sect.Children[0]
		for p != nil {
			for i := 0; i < p.Level; i++ {
				text = append(text, []byte("#")...)
			}

			text = append(text, []byte(" ")...)
			text = append(text, []byte(p.Title)...)
			text = append(text, []byte("\n\n")...)
			text = append(text, []byte(p.Text)...)
			text = append(text, []byte("\n\n")...)
			p = mdast.Next(p, sect)
		}
		md += string(text)
	}
	return []byte(md)
}
