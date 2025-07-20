# Real-Time Technical Architecture
*WorldBox-style engine for cosmic civilization simulation*

## Engine Overview

### Core Architecture Philosophy
- **Real-Time First**: Everything updates continuously, not turn-based
- **Observable Reality**: Visual representation matches simulation state exactly
- **Scalable Performance**: Handle millions of entities across cosmic scales
- **Emergent Complexity**: Simple rules create complex behaviors
- **Immediate Feedback**: Player actions have instant visual results

## System Architecture

### Main Engine Components
```
┌─────────────────────────────────────────────────┐
│                 Presentation Layer              │ 60 FPS
├─────────────────────────────────────────────────┤
│                Game Logic Layer                 │ 60 FPS
├─────────────────────────────────────────────────┤
│              Simulation Engine Core             │ Variable
├─────────────────────────────────────────────────┤
│                Entity Management                │ Variable
├─────────────────────────────────────────────────┤
│               Performance Systems               │ Background
└─────────────────────────────────────────────────┘
```

### Thread Architecture
```
MAIN THREAD (60 FPS)
- Input processing
- UI updates
- Render commands
- Audio triggers

SIMULATION THREAD (Variable Hz)
- Entity updates
- AI decisions
- Physics simulation
- Event processing

BACKGROUND THREADS
- Path finding
- Texture streaming
- Save operations
- Network sync (multiplayer)
```

## Entity System

### Component-Based Architecture
```cpp
// Core entity structure
struct Entity {
    EntityID id;
    ComponentMask components;
    SpatialHash spatial_location;
    UpdateFrequency update_rate;
};

// Key components
struct Transform {
    Vector2 position;
    float rotation;
    float scale;
};

struct Sprite {
    TextureID texture;
    Color tint;
    AnimationState animation;
};

struct UnitAI {
    Needs current_needs;
    Personality traits;
    DecisionTree behavior;
    float last_update_time;
};

struct CivilizationMember {
    CivilizationID civ_id;
    Role role;
    SocialConnections relationships;
    KnowledgeState knowledge;
};
```

### Entity Pools and Management
```cpp
class EntityManager {
private:
    // Pool allocators for different entity types
    ObjectPool<Unit> unit_pool;
    ObjectPool<Building> building_pool;
    ObjectPool<Effect> effect_pool;
    
    // Spatial partitioning for efficient queries
    SpatialHash<Entity> spatial_grid;
    
    // Update scheduling
    PriorityQueue<EntityUpdate> update_queue;
    
public:
    Entity* create_entity(EntityType type);
    void destroy_entity(EntityID id);
    std::vector<Entity*> query_region(BoundingBox region);
    void schedule_update(EntityID id, float when);
};
```

## Multi-Scale Simulation

### Level of Detail System
```cpp
enum class SimulationDetail {
    FULL,      // Individual unit AI, all systems
    MEDIUM,    // Group behaviors, simplified AI
    LOW,       // Statistical only
    SLEEPING   // No updates, state preserved
};

class LODManager {
private:
    Camera player_camera;
    float detail_distance_thresholds[4];
    
public:
    SimulationDetail calculate_lod(const Entity& entity) {
        float distance = distance_to_camera(entity.position);
        float importance = entity.importance_score;
        
        // Closer objects get higher detail
        // Important objects (capitals, heroes) always high detail
        if (distance < detail_distance_thresholds[0] || importance > 0.8f)
            return SimulationDetail::FULL;
        else if (distance < detail_distance_thresholds[1])
            return SimulationDetail::MEDIUM;
        else if (distance < detail_distance_thresholds[2])
            return SimulationDetail::LOW;
        else
            return SimulationDetail::SLEEPING;
    }
};
```

### Time Scaling System
```cpp
class TimeManager {
private:
    float global_time_scale = 1.0f;
    std::map<Region, float> regional_time_scales;
    bool paused = false;
    
public:
    float get_delta_time_for_entity(const Entity& entity) {
        if (paused) return 0.0f;
        
        float base_dt = engine.get_delta_time();
        float global_scale = global_time_scale;
        float regional_scale = get_regional_scale(entity.position);
        
        return base_dt * global_scale * regional_scale;
    }
    
    void set_time_scale(float scale) { global_time_scale = scale; }
    void set_regional_scale(Region region, float scale) {
        regional_time_scales[region] = scale;
    }
};
```

## AI System Architecture

### Hierarchical AI Updates
```cpp
class AISystem {
private:
    // Different update frequencies for different AI levels
    float individual_ai_hz = 10.0f;   // 10 times per second
    float group_ai_hz = 1.0f;         // Once per second
    float civilization_ai_hz = 0.1f;  // Once per 10 seconds
    
public:
    void update_individual_ai(Entity& unit, float dt) {
        // Personal needs, immediate decisions
        update_needs(unit);
        update_pathfinding(unit);
        execute_current_action(unit);
    }
    
    void update_group_ai(std::vector<Entity*>& group, float dt) {
        // Collective behaviors, coordination
        update_group_goals(group);
        coordinate_actions(group);
        handle_group_conflicts(group);
    }
    
    void update_civilization_ai(Civilization& civ, float dt) {
        // High-level strategy, research, diplomacy
        update_research_priorities(civ);
        process_diplomatic_actions(civ);
        plan_expansion_strategy(civ);
    }
};
```

### Need-Based Decision System
```cpp
class NeedsSystem {
private:
    struct Need {
        NeedType type;
        float urgency;    // 0.0 to 1.0
        float satisfaction; // 0.0 to 1.0
        float decay_rate;
    };
    
public:
    void update_needs(Entity& unit, float dt) {
        for (auto& need : unit.get_component<UnitAI>().needs) {
            // Needs decay over time
            need.satisfaction -= need.decay_rate * dt;
            need.satisfaction = std::max(0.0f, need.satisfaction);
            
            // Calculate urgency based on satisfaction and personality
            need.urgency = calculate_urgency(need, unit.personality);
        }
        
        // Sort needs by urgency
        sort_needs_by_urgency(unit);
    }
    
private:
    float calculate_urgency(const Need& need, const Personality& personality) {
        float base_urgency = 1.0f - need.satisfaction;
        
        // Personality modifiers
        switch (need.type) {
            case NeedType::FOOD:
                return base_urgency * (1.0f + personality.survival_focus);
            case NeedType::SOCIAL:
                return base_urgency * (1.0f + personality.social_tendency);
            case NeedType::EXPLORATION:
                return base_urgency * (1.0f + personality.curiosity);
            // ... etc
        }
        
        return base_urgency;
    }
};
```

## Rendering System

### Sprite Batching System
```cpp
class SpriteRenderer {
private:
    struct SpriteBatch {
        TextureID texture;
        std::vector<SpriteInstance> instances;
        VertexBuffer vertex_buffer;
        IndexBuffer index_buffer;
    };
    
    std::map<TextureID, SpriteBatch> batches;
    
public:
    void submit_sprite(const Sprite& sprite, const Transform& transform) {
        auto& batch = batches[sprite.texture];
        batch.instances.push_back({
            .position = transform.position,
            .rotation = transform.rotation,
            .scale = transform.scale,
            .uv_rect = sprite.uv_rect,
            .color = sprite.color
        });
    }
    
    void render_all_batches() {
        for (auto& [texture_id, batch] : batches) {
            update_vertex_buffer(batch);
            bind_texture(texture_id);
            draw_instanced(batch.vertex_buffer, batch.instances.size());
            batch.instances.clear();
        }
    }
};
```

### Dynamic Camera System
```cpp
class CameraSystem {
private:
    Vector2 position;
    float zoom_level = 1.0f;
    float min_zoom = 0.1f;   // Galactic view
    float max_zoom = 10.0f;  // Individual unit view
    
public:
    void update_zoom(float zoom_delta) {
        zoom_level *= (1.0f + zoom_delta);
        zoom_level = std::clamp(zoom_level, min_zoom, max_zoom);
        
        // Adjust simulation detail based on zoom
        update_simulation_detail_for_zoom();
    }
    
    BoundingBox get_visible_region() const {
        float width = screen_width / zoom_level;
        float height = screen_height / zoom_level;
        return BoundingBox{
            position.x - width/2, position.y - height/2,
            width, height
        };
    }
    
private:
    void update_simulation_detail_for_zoom() {
        // Higher zoom = more detail needed
        float detail_multiplier = zoom_level / max_zoom;
        LODManager::set_detail_bias(detail_multiplier);
    }
};
```

## Performance Optimization

### Spatial Partitioning
```cpp
class SpatialHash {
private:
    static constexpr float CELL_SIZE = 64.0f; // pixels
    std::unordered_map<CellID, std::vector<EntityID>> cells;
    
public:
    void insert(EntityID entity, Vector2 position) {
        CellID cell = position_to_cell(position);
        cells[cell].push_back(entity);
    }
    
    std::vector<EntityID> query_circle(Vector2 center, float radius) {
        std::vector<EntityID> results;
        
        // Check all cells that might intersect
        int min_x = (center.x - radius) / CELL_SIZE;
        int max_x = (center.x + radius) / CELL_SIZE;
        int min_y = (center.y - radius) / CELL_SIZE;
        int max_y = (center.y + radius) / CELL_SIZE;
        
        for (int x = min_x; x <= max_x; ++x) {
            for (int y = min_y; y <= max_y; ++y) {
                CellID cell = {x, y};
                if (auto it = cells.find(cell); it != cells.end()) {
                    for (EntityID id : it->second) {
                        if (distance(center, get_position(id)) <= radius) {
                            results.push_back(id);
                        }
                    }
                }
            }
        }
        
        return results;
    }
};
```

### Async Pathfinding
```cpp
class PathfindingSystem {
private:
    ThreadPool pathfinding_threads;
    std::queue<PathRequest> request_queue;
    std::map<EntityID, PathResult> completed_paths;
    
public:
    void request_path(EntityID entity, Vector2 start, Vector2 goal) {
        PathRequest request{entity, start, goal, high_priority(entity)};
        request_queue.push(request);
    }
    
    void process_requests() {
        while (!request_queue.empty() && pathfinding_threads.has_available()) {
            auto request = request_queue.front();
            request_queue.pop();
            
            // Submit to thread pool
            pathfinding_threads.submit([=]() {
                auto path = calculate_astar_path(request.start, request.goal);
                completed_paths[request.entity] = path;
            });
        }
    }
    
    std::optional<Path> get_completed_path(EntityID entity) {
        if (auto it = completed_paths.find(entity); it != completed_paths.end()) {
            auto path = it->second;
            completed_paths.erase(it);
            return path;
        }
        return std::nullopt;
    }
};
```

## Memory Management

### Object Pooling
```cpp
template<typename T>
class ObjectPool {
private:
    std::vector<T> objects;
    std::stack<size_t> available_indices;
    size_t next_index = 0;
    
public:
    T* acquire() {
        if (!available_indices.empty()) {
            size_t index = available_indices.top();
            available_indices.pop();
            return &objects[index];
        } else {
            if (next_index >= objects.size()) {
                objects.resize(objects.size() * 2);
            }
            return &objects[next_index++];
        }
    }
    
    void release(T* object) {
        size_t index = object - &objects[0];
        object->~T();
        new(object) T(); // Reset to default state
        available_indices.push(index);
    }
};
```

### Streaming System
```cpp
class WorldStreamer {
private:
    LRUCache<ChunkID, WorldChunk> loaded_chunks;
    ThreadPool loading_threads;
    
public:
    void update_around_camera(Vector2 camera_pos) {
        ChunkID center_chunk = position_to_chunk(camera_pos);
        
        // Load chunks in spiral around camera
        for (int radius = 0; radius <= LOAD_RADIUS; ++radius) {
            for (auto chunk_id : get_chunks_at_radius(center_chunk, radius)) {
                if (!loaded_chunks.contains(chunk_id)) {
                    request_chunk_load(chunk_id);
                }
            }
        }
        
        // Unload distant chunks
        auto far_chunks = loaded_chunks.get_items_beyond_distance(
            center_chunk, UNLOAD_RADIUS);
        for (auto chunk_id : far_chunks) {
            unload_chunk(chunk_id);
        }
    }
};
```

## Save/Load System

### Incremental Saves
```cpp
class SaveSystem {
private:
    WorldState last_saved_state;
    std::vector<StateChange> changes_since_save;
    
public:
    void record_change(const StateChange& change) {
        changes_since_save.push_back(change);
        
        // Auto-save if too many changes accumulated
        if (changes_since_save.size() > MAX_CHANGES_BEFORE_SAVE) {
            save_incremental();
        }
    }
    
    void save_incremental() {
        SaveFile save;
        save.base_state = last_saved_state;
        save.changes = changes_since_save;
        save.timestamp = get_current_time();
        
        async_write_to_disk(save);
        
        // Update baseline
        apply_changes_to_state(last_saved_state, changes_since_save);
        changes_since_save.clear();
    }
};
```

## Platform-Specific Optimizations

### Multi-Threading Strategy
```cpp
class PlatformOptimizer {
public:
    void initialize() {
        int cpu_cores = std::thread::hardware_concurrency();
        
        // Reserve threads based on available cores
        if (cpu_cores >= 8) {
            // High-end: Dedicated threads for different systems
            simulation_threads = 4;
            rendering_threads = 2;
            io_threads = 2;
        } else if (cpu_cores >= 4) {
            // Mid-range: Shared simulation threads
            simulation_threads = 2;
            rendering_threads = 1;
            io_threads = 1;
        } else {
            // Low-end: Single simulation thread
            simulation_threads = 1;
            rendering_threads = 0; // Use main thread
            io_threads = 1;
        }
    }
};
```

This architecture provides the foundation for a living, breathing universe that runs smoothly while maintaining the emergent complexity and visual appeal that makes WorldBox so engaging to watch. The key is balancing simulation depth with performance, ensuring the world feels alive without overwhelming the hardware.