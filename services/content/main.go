package main

import (
	"crypto/rand"
	"fmt"

	"encoding/json"
	"log"
	"net/http"
	"os"
	"strings"
	"sync"
)

// Data models

type Course struct {
	ID          string   `json:"id"`
	Title       string   `json:"title"`
	Description string   `json:"description,omitempty"`
	Language    string   `json:"language"`
	Status      string   `json:"status"`
	Visibility  string   `json:"visibility"`
	Tags        []string `json:"tags,omitempty"`
}

type Section struct {
	ID       string `json:"id"`
	CourseID string `json:"course_id"`
	Title    string `json:"title"`
	Sequence int    `json:"sequence"`
}

type Material struct {
	ID        string `json:"id"`
	SectionID string `json:"section_id"`
	Type      string `json:"type"`
	Title     string `json:"title"`
	Status    string `json:"status"`
}

// In-memory store

type store struct {
	mu        sync.RWMutex
	courses   map[string]Course
	sections  map[string]Section
	materials map[string]Material
}

var s = store{
	courses:   make(map[string]Course),
	sections:  make(map[string]Section),
	materials: make(map[string]Material),
}

func genID() string {
	b := make([]byte, 16)
	if _, err := rand.Read(b); err != nil {
		panic(err)
	}
	return fmt.Sprintf("%x-%x-%x-%x-%x", b[0:4], b[4:6], b[6:8], b[8:10], b[10:16])
}

var swaggerSpec []byte

func main() {
	mux := http.NewServeMux()

	data, err := os.ReadFile("swagger.json")
	if err == nil {
		swaggerSpec = data
	} else {
		log.Printf("unable to read swagger.json: %v", err)
	}

	mux.HandleFunc("/docs", docsHandler)
	mux.HandleFunc("/docs/swagger.json", specHandler)

	mux.HandleFunc("/api/courses", handleCourses)
	mux.HandleFunc("/api/courses/", handleCourseSubroutes)
	mux.HandleFunc("/api/sections/", handleSectionSubroutes)
	mux.HandleFunc("/api/materials/", handleMaterialByID)
	mux.HandleFunc("/api/media/", handleMedia)

	log.Println("Content Service listening on :8000")
	if err := http.ListenAndServe(":8000", mux); err != nil {
		log.Fatal(err)
	}
}

// ---- Course handlers ----

func handleCourses(w http.ResponseWriter, r *http.Request) {
	switch r.Method {
	case http.MethodGet:
		listCourses(w, r)
	case http.MethodPost:
		createCourse(w, r)
	default:
		http.Error(w, "method not allowed", http.StatusMethodNotAllowed)
	}
}

func handleCourseSubroutes(w http.ResponseWriter, r *http.Request) {
	path := strings.TrimPrefix(r.URL.Path, "/api/courses/")
	if strings.HasSuffix(path, "/sections") {
		id := strings.TrimSuffix(path, "/sections")
		if r.Method == http.MethodGet {
			listSections(w, r, id)
			return
		} else if r.Method == http.MethodPost {
			createSection(w, r, id)
			return
		}
	}
	id := strings.Trim(path, "/")
	switch r.Method {
	case http.MethodGet:
		getCourse(w, r, id)
	case http.MethodPut:
		updateCourse(w, r, id)
	case http.MethodDelete:
		deleteCourse(w, r, id)
	default:
		http.Error(w, "method not allowed", http.StatusMethodNotAllowed)
	}
}

func listCourses(w http.ResponseWriter, r *http.Request) {
	s.mu.RLock()
	defer s.mu.RUnlock()
	arr := make([]Course, 0, len(s.courses))
	for _, c := range s.courses {
		arr = append(arr, c)
	}
	json.NewEncoder(w).Encode(arr)
}

func createCourse(w http.ResponseWriter, r *http.Request) {
	var c Course
	if err := json.NewDecoder(r.Body).Decode(&c); err != nil {
		http.Error(w, "bad request", http.StatusBadRequest)
		return
	}
	if c.Title == "" {
		http.Error(w, "title required", http.StatusBadRequest)
		return
	}
	c.ID = genID()
	if c.Status == "" {
		c.Status = "draft"
	}
	if c.Visibility == "" {
		c.Visibility = "private"
	}
	s.mu.Lock()
	s.courses[c.ID] = c
	s.mu.Unlock()
	w.WriteHeader(http.StatusCreated)
	json.NewEncoder(w).Encode(c)
}

func getCourse(w http.ResponseWriter, r *http.Request, id string) {
	s.mu.RLock()
	c, ok := s.courses[id]
	s.mu.RUnlock()
	if !ok {
		http.NotFound(w, r)
		return
	}
	json.NewEncoder(w).Encode(c)
}

func updateCourse(w http.ResponseWriter, r *http.Request, id string) {
	var upd Course
	if err := json.NewDecoder(r.Body).Decode(&upd); err != nil {
		http.Error(w, "bad request", http.StatusBadRequest)
		return
	}
	s.mu.Lock()
	c, ok := s.courses[id]
	if !ok {
		s.mu.Unlock()
		http.NotFound(w, r)
		return
	}
	if upd.Title != "" {
		c.Title = upd.Title
	}
	if upd.Description != "" {
		c.Description = upd.Description
	}
	if upd.Status != "" {
		c.Status = upd.Status
	}
	if upd.Visibility != "" {
		c.Visibility = upd.Visibility
	}
	if len(upd.Tags) > 0 {
		c.Tags = upd.Tags
	}
	s.courses[id] = c
	s.mu.Unlock()
	json.NewEncoder(w).Encode(c)
}

func deleteCourse(w http.ResponseWriter, r *http.Request, id string) {
	s.mu.Lock()
	delete(s.courses, id)
	s.mu.Unlock()
	w.WriteHeader(http.StatusNoContent)
}

// ---- Section handlers ----

func listSections(w http.ResponseWriter, r *http.Request, courseID string) {
	s.mu.RLock()
	defer s.mu.RUnlock()
	arr := []Section{}
	for _, sec := range s.sections {
		if sec.CourseID == courseID {
			arr = append(arr, sec)
		}
	}
	json.NewEncoder(w).Encode(arr)
}

func createSection(w http.ResponseWriter, r *http.Request, courseID string) {
	var sec Section
	if err := json.NewDecoder(r.Body).Decode(&sec); err != nil {
		http.Error(w, "bad request", http.StatusBadRequest)
		return
	}
	if sec.Title == "" {
		http.Error(w, "title required", http.StatusBadRequest)
		return
	}
	sec.ID = genID()
	sec.CourseID = courseID
	s.mu.Lock()
	s.sections[sec.ID] = sec
	s.mu.Unlock()
	w.WriteHeader(http.StatusCreated)
	json.NewEncoder(w).Encode(sec)
}

func handleSectionSubroutes(w http.ResponseWriter, r *http.Request) {
	path := strings.TrimPrefix(r.URL.Path, "/api/sections/")
	if strings.HasSuffix(path, "/materials") {
		id := strings.TrimSuffix(path, "/materials")
		if r.Method == http.MethodGet {
			listMaterials(w, r, id)
			return
		} else if r.Method == http.MethodPost {
			createMaterial(w, r, id)
			return
		}
	}
	id := strings.Trim(path, "/")
	switch r.Method {
	case http.MethodPut:
		updateSection(w, r, id)
	case http.MethodDelete:
		deleteSection(w, r, id)
	default:
		http.Error(w, "method not allowed", http.StatusMethodNotAllowed)
	}
}

func updateSection(w http.ResponseWriter, r *http.Request, id string) {
	var upd Section
	if err := json.NewDecoder(r.Body).Decode(&upd); err != nil {
		http.Error(w, "bad request", http.StatusBadRequest)
		return
	}
	s.mu.Lock()
	sec, ok := s.sections[id]
	if !ok {
		s.mu.Unlock()
		http.NotFound(w, r)
		return
	}
	if upd.Title != "" {
		sec.Title = upd.Title
	}
	if upd.Sequence != 0 {
		sec.Sequence = upd.Sequence
	}
	s.sections[id] = sec
	s.mu.Unlock()
	json.NewEncoder(w).Encode(sec)
}

func deleteSection(w http.ResponseWriter, r *http.Request, id string) {
	s.mu.Lock()
	delete(s.sections, id)
	s.mu.Unlock()
	w.WriteHeader(http.StatusNoContent)
}

// ---- Material handlers ----

func listMaterials(w http.ResponseWriter, r *http.Request, sectionID string) {
	s.mu.RLock()
	defer s.mu.RUnlock()
	arr := []Material{}
	for _, m := range s.materials {
		if m.SectionID == sectionID {
			arr = append(arr, m)
		}
	}
	json.NewEncoder(w).Encode(arr)
}

func createMaterial(w http.ResponseWriter, r *http.Request, sectionID string) {
	var m Material
	if err := json.NewDecoder(r.Body).Decode(&m); err != nil {
		http.Error(w, "bad request", http.StatusBadRequest)
		return
	}
	if m.Title == "" || m.Type == "" {
		http.Error(w, "title and type required", http.StatusBadRequest)
		return
	}
	m.ID = genID()
	m.SectionID = sectionID
	if m.Status == "" {
		m.Status = "draft"
	}
	s.mu.Lock()
	s.materials[m.ID] = m
	s.mu.Unlock()
	w.WriteHeader(http.StatusCreated)
	json.NewEncoder(w).Encode(m)
}

func handleMaterialByID(w http.ResponseWriter, r *http.Request) {
	id := strings.TrimPrefix(r.URL.Path, "/api/materials/")
	switch r.Method {
	case http.MethodPut:
		updateMaterial(w, r, id)
	case http.MethodDelete:
		deleteMaterial(w, r, id)
	default:
		http.Error(w, "method not allowed", http.StatusMethodNotAllowed)
	}
}

func updateMaterial(w http.ResponseWriter, r *http.Request, id string) {
	var upd Material
	if err := json.NewDecoder(r.Body).Decode(&upd); err != nil {
		http.Error(w, "bad request", http.StatusBadRequest)
		return
	}
	s.mu.Lock()
	mat, ok := s.materials[id]
	if !ok {
		s.mu.Unlock()
		http.NotFound(w, r)
		return
	}
	if upd.Title != "" {
		mat.Title = upd.Title
	}
	if upd.Status != "" {
		mat.Status = upd.Status
	}
	s.materials[id] = mat
	s.mu.Unlock()
	json.NewEncoder(w).Encode(mat)
}

func deleteMaterial(w http.ResponseWriter, r *http.Request, id string) {
	s.mu.Lock()
	delete(s.materials, id)
	s.mu.Unlock()
	w.WriteHeader(http.StatusNoContent)
}

// ---- Media placeholder ----

type MediaStatus struct {
	MediaFileID string `json:"media_file_id"`
	Status      string `json:"status"`
	URL         string `json:"url,omitempty"`
}

func handleMedia(w http.ResponseWriter, r *http.Request) {
	id := strings.TrimPrefix(r.URL.Path, "/api/media/")
	if strings.HasSuffix(id, "/status") {
		mediaID := strings.TrimSuffix(id, "/status")
		json.NewEncoder(w).Encode(MediaStatus{MediaFileID: mediaID, Status: "queued"})
		return
	}
	if strings.HasSuffix(id, "/stream") {
		http.Redirect(w, r, "https://example.com/stream/"+strings.TrimSuffix(id, "/stream"), http.StatusFound)
		return
	}
	http.NotFound(w, r)
}

func specHandler(w http.ResponseWriter, r *http.Request) {
	if swaggerSpec == nil {
		http.Error(w, "spec not found", http.StatusNotFound)
		return
	}
	w.Header().Set("Content-Type", "application/json")
	w.Write(swaggerSpec)
}

func docsHandler(w http.ResponseWriter, r *http.Request) {
	w.Header().Set("Content-Type", "text/html; charset=utf-8")
	fmt.Fprint(w, `<!DOCTYPE html>
<html>
<head>
  <title>Content Service API</title>
  <link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/swagger-ui-dist@4/swagger-ui.css" />
</head>
<body>
<div id="swagger-ui"></div>
<script src="https://cdn.jsdelivr.net/npm/swagger-ui-dist@4/swagger-ui-bundle.js"></script>
<script>
window.onload = function() {
  SwaggerUIBundle({url: 'swagger.json', dom_id: '#swagger-ui'});
};
</script>
</body>
</html>`)
}
