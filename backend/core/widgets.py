"""
Custom SQLAdmin widgets for the portfolio admin panel.

This module contains custom form widgets for:
- TypeSelectorWidget: Radio buttons for Static/External project type selection
- CodeEditorWidget: Textarea with syntax highlighting for HTML/CSS/JS
- StatusToggleWidget: Toggle switch for Live/Draft status
- ZipUploadWidget: Drag-drop zone for ZIP file uploads
"""

from markupsafe import Markup
from wtforms.widgets import TextInput, TextArea


class TypeSelectorWidget(TextInput):
    """
    Custom widget for selecting project type (Static/External).
    
    Displays radio buttons and uses JavaScript to show/hide conditional fields:
    - Static: shows code editor and ZIP upload fields
    - External: shows external URL field
    
    Requirements: 2.1, 2.2, 2.3
    """
    
    def __call__(self, field, **kwargs):
        field_id = field.id
        field_name = field.name
        current_value = field.data or 'external'
        
        static_checked = 'checked' if current_value == 'static' else ''
        external_checked = 'checked' if current_value == 'external' else ''
        
        return Markup(f'''
            <div class="type-selector-widget" id="type_selector_{field_id}">
                <div style="display:flex;gap:20px;margin-bottom:15px;">
                    <label style="display:flex;align-items:center;gap:8px;cursor:pointer;
                                  padding:12px 20px;border-radius:8px;
                                  background:{('#6366f1' if current_value == 'static' else '#1f2937')};
                                  border:2px solid {('#6366f1' if current_value == 'static' else '#374151')};
                                  transition:all 0.2s ease;">
                        <input type="radio" name="{field_name}" value="static" 
                               {static_checked}
                               onchange="handleTypeChange_{field_id}(this)"
                               style="width:18px;height:18px;accent-color:#6366f1;">
                        <span style="font-weight:500;">
                            <i class="fa-solid fa-code" style="margin-right:6px;"></i>
                            Static (Light)
                        </span>
                    </label>
                    
                    <label style="display:flex;align-items:center;gap:8px;cursor:pointer;
                                  padding:12px 20px;border-radius:8px;
                                  background:{('#6366f1' if current_value == 'external' else '#1f2937')};
                                  border:2px solid {('#6366f1' if current_value == 'external' else '#374151')};
                                  transition:all 0.2s ease;">
                        <input type="radio" name="{field_name}" value="external" 
                               {external_checked}
                               onchange="handleTypeChange_{field_id}(this)"
                               style="width:18px;height:18px;accent-color:#6366f1;">
                        <span style="font-weight:500;">
                            <i class="fa-solid fa-link" style="margin-right:6px;"></i>
                            External (Complex)
                        </span>
                    </label>
                </div>
                
                <p id="type_hint_{field_id}" style="color:#9ca3af;font-size:0.875rem;margin:0;">
                    {('Static projects store HTML/CSS/JS code or ZIP archives locally.' 
                      if current_value == 'static' 
                      else 'External projects link to hosted resources via URL.')}
                </p>
            </div>
            
            <script>
                function handleTypeChange_{field_id}(radio) {{
                    const container = document.getElementById('type_selector_{field_id}');
                    const labels = container.querySelectorAll('label');
                    const hint = document.getElementById('type_hint_{field_id}');
                    
                    labels.forEach(label => {{
                        const input = label.querySelector('input');
                        if (input.checked) {{
                            label.style.background = '#6366f1';
                            label.style.borderColor = '#6366f1';
                        }} else {{
                            label.style.background = '#1f2937';
                            label.style.borderColor = '#374151';
                        }}
                    }});
                    
                    // Update hint text
                    if (radio.value === 'static') {{
                        hint.textContent = 'Static projects store HTML/CSS/JS code or ZIP archives locally.';
                    }} else {{
                        hint.textContent = 'External projects link to hosted resources via URL.';
                    }}
                    
                    // Show/hide conditional fields
                    toggleConditionalFields_{field_id}(radio.value);
                }}
                
                function toggleConditionalFields_{field_id}(type) {{
                    // Find static-related fields
                    const staticContentField = document.querySelector('[name="static_content"]')?.closest('.col-md-6, .mb-3, .form-group');
                    const staticPathField = document.querySelector('[name="static_path"]')?.closest('.col-md-6, .mb-3, .form-group');
                    const zipUploadField = document.getElementById('zip_upload_container');
                    
                    // Find external-related fields
                    const liveUrlField = document.querySelector('[name="live_url"]')?.closest('.col-md-6, .mb-3, .form-group');
                    
                    if (type === 'static') {{
                        // Show static fields
                        if (staticContentField) staticContentField.style.display = '';
                        if (staticPathField) staticPathField.style.display = '';
                        if (zipUploadField) zipUploadField.style.display = '';
                        
                        // Hide external fields (but keep live_url visible for reference)
                        // if (liveUrlField) liveUrlField.style.display = 'none';
                    }} else {{
                        // Hide static fields
                        if (staticContentField) staticContentField.style.display = 'none';
                        if (staticPathField) staticPathField.style.display = 'none';
                        if (zipUploadField) zipUploadField.style.display = 'none';
                        
                        // Show external fields
                        if (liveUrlField) liveUrlField.style.display = '';
                    }}
                }}
                
                // Initialize on page load
                document.addEventListener('DOMContentLoaded', function() {{
                    const currentType = document.querySelector('input[name="{field_name}"]:checked')?.value || 'external';
                    toggleConditionalFields_{field_id}(currentType);
                }});
            </script>
        ''')



class CodeEditorWidget(TextArea):
    """
    Custom widget for editing HTML/CSS/JS code with syntax highlighting.
    
    Uses CodeMirror for syntax highlighting with support for:
    - HTML mode
    - CSS mode  
    - JavaScript mode
    - Mixed HTML mode (for embedded CSS/JS)
    
    Requirements: 2.2, 6.2
    """
    
    def __call__(self, field, **kwargs):
        field_id = field.id
        field_name = field.name
        current_value = field.data or ''
        
        # Escape the content for safe embedding in HTML
        escaped_value = (current_value
                        .replace('&', '&amp;')
                        .replace('<', '&lt;')
                        .replace('>', '&gt;')
                        .replace('"', '&quot;')
                        .replace("'", '&#39;')
                        .replace('`', '&#96;'))
        
        return Markup(f'''
            <div class="code-editor-widget" id="code_editor_container_{field_id}">
                <!-- Mode selector -->
                <div style="display:flex;gap:10px;margin-bottom:10px;align-items:center;">
                    <span style="color:#9ca3af;font-size:0.875rem;">Syntax:</span>
                    <select id="mode_selector_{field_id}" 
                            onchange="changeEditorMode_{field_id}(this.value)"
                            style="background:#1f2937;border:1px solid #374151;border-radius:4px;
                                   padding:4px 8px;color:#e5e7eb;font-size:0.875rem;">
                        <option value="htmlmixed">HTML (Mixed)</option>
                        <option value="css">CSS</option>
                        <option value="javascript">JavaScript</option>
                    </select>
                    <button type="button" onclick="formatCode_{field_id}()"
                            style="background:#374151;border:none;border-radius:4px;
                                   padding:4px 12px;color:#e5e7eb;cursor:pointer;font-size:0.875rem;">
                        <i class="fa-solid fa-indent"></i> Format
                    </button>
                    <button type="button" onclick="clearCode_{field_id}()"
                            style="background:#374151;border:none;border-radius:4px;
                                   padding:4px 12px;color:#e5e7eb;cursor:pointer;font-size:0.875rem;">
                        <i class="fa-solid fa-trash"></i> Clear
                    </button>
                </div>
                
                <!-- Hidden textarea for form submission -->
                <textarea name="{field_name}" id="{field_id}" 
                          style="display:none;">{escaped_value}</textarea>
                
                <!-- CodeMirror container -->
                <div id="codemirror_{field_id}" 
                     style="border:1px solid #374151;border-radius:8px;overflow:hidden;"></div>
                
                <!-- Character count -->
                <div style="display:flex;justify-content:space-between;margin-top:8px;
                            color:#6b7280;font-size:0.75rem;">
                    <span id="char_count_{field_id}">0 characters</span>
                    <span>Ctrl+S to save, Ctrl+F to search</span>
                </div>
            </div>
            
            <!-- Load CodeMirror from CDN -->
            <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/codemirror/5.65.16/codemirror.min.css">
            <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/codemirror/5.65.16/theme/dracula.min.css">
            <script src="https://cdnjs.cloudflare.com/ajax/libs/codemirror/5.65.16/codemirror.min.js"></script>
            <script src="https://cdnjs.cloudflare.com/ajax/libs/codemirror/5.65.16/mode/xml/xml.min.js"></script>
            <script src="https://cdnjs.cloudflare.com/ajax/libs/codemirror/5.65.16/mode/javascript/javascript.min.js"></script>
            <script src="https://cdnjs.cloudflare.com/ajax/libs/codemirror/5.65.16/mode/css/css.min.js"></script>
            <script src="https://cdnjs.cloudflare.com/ajax/libs/codemirror/5.65.16/mode/htmlmixed/htmlmixed.min.js"></script>
            <script src="https://cdnjs.cloudflare.com/ajax/libs/codemirror/5.65.16/addon/edit/closetag.min.js"></script>
            <script src="https://cdnjs.cloudflare.com/ajax/libs/codemirror/5.65.16/addon/edit/closebrackets.min.js"></script>
            <script src="https://cdnjs.cloudflare.com/ajax/libs/codemirror/5.65.16/addon/search/search.min.js"></script>
            <script src="https://cdnjs.cloudflare.com/ajax/libs/codemirror/5.65.16/addon/search/searchcursor.min.js"></script>
            <script src="https://cdnjs.cloudflare.com/ajax/libs/codemirror/5.65.16/addon/dialog/dialog.min.js"></script>
            <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/codemirror/5.65.16/addon/dialog/dialog.min.css">
            
            <script>
                var editor_{field_id};
                
                document.addEventListener('DOMContentLoaded', function() {{
                    const textarea = document.getElementById('{field_id}');
                    const container = document.getElementById('codemirror_{field_id}');
                    
                    editor_{field_id} = CodeMirror(container, {{
                        value: textarea.value,
                        mode: 'htmlmixed',
                        theme: 'dracula',
                        lineNumbers: true,
                        lineWrapping: true,
                        autoCloseTags: true,
                        autoCloseBrackets: true,
                        indentUnit: 2,
                        tabSize: 2,
                        indentWithTabs: false,
                        extraKeys: {{
                            'Ctrl-S': function(cm) {{
                                // Trigger form save
                                const form = document.querySelector('form');
                                if (form) form.submit();
                            }},
                            'Tab': function(cm) {{
                                cm.replaceSelection('  ', 'end');
                            }}
                        }}
                    }});
                    
                    editor_{field_id}.setSize(null, 400);
                    
                    // Sync to hidden textarea on change
                    editor_{field_id}.on('change', function(cm) {{
                        textarea.value = cm.getValue();
                        updateCharCount_{field_id}();
                    }});
                    
                    updateCharCount_{field_id}();
                }});
                
                function changeEditorMode_{field_id}(mode) {{
                    if (editor_{field_id}) {{
                        editor_{field_id}.setOption('mode', mode);
                    }}
                }}
                
                function formatCode_{field_id}() {{
                    if (editor_{field_id}) {{
                        const totalLines = editor_{field_id}.lineCount();
                        editor_{field_id}.autoFormatRange(
                            {{line: 0, ch: 0}},
                            {{line: totalLines}}
                        );
                    }}
                }}
                
                function clearCode_{field_id}() {{
                    if (editor_{field_id} && confirm('Clear all code?')) {{
                        editor_{field_id}.setValue('');
                    }}
                }}
                
                function updateCharCount_{field_id}() {{
                    const count = document.getElementById('{field_id}').value.length;
                    document.getElementById('char_count_{field_id}').textContent = count + ' characters';
                }}
            </script>
            
            <style>
                #codemirror_{field_id} .CodeMirror {{
                    font-family: 'JetBrains Mono', 'Fira Code', monospace;
                    font-size: 14px;
                }}
            </style>
        ''')



class StatusToggleWidget(TextInput):
    """
    Custom widget for toggling project status between Live and Draft.
    
    Displays a toggle switch with color indication:
    - Live: green (#22c55e)
    - Draft: gray (#6b7280)
    
    Requirements: 3.5
    """
    
    def __call__(self, field, **kwargs):
        field_id = field.id
        field_name = field.name
        current_value = field.data or 'draft'
        
        is_live = current_value == 'live'
        
        return Markup(f'''
            <div class="status-toggle-widget" id="status_toggle_{field_id}">
                <!-- Hidden input for form submission -->
                <input type="hidden" name="{field_name}" id="{field_id}" value="{current_value}">
                
                <div style="display:flex;align-items:center;gap:15px;">
                    <!-- Toggle switch -->
                    <div class="toggle-container" 
                         onclick="toggleStatus_{field_id}()"
                         style="position:relative;width:60px;height:32px;
                                background:{('#22c55e' if is_live else '#374151')};
                                border-radius:16px;cursor:pointer;
                                transition:background 0.3s ease;
                                box-shadow:inset 0 2px 4px rgba(0,0,0,0.2);">
                        <div id="toggle_knob_{field_id}"
                             style="position:absolute;top:3px;
                                    left:{('31px' if is_live else '3px')};
                                    width:26px;height:26px;
                                    background:white;border-radius:50%;
                                    transition:left 0.3s ease;
                                    box-shadow:0 2px 4px rgba(0,0,0,0.2);"></div>
                    </div>
                    
                    <!-- Status label -->
                    <div id="status_label_{field_id}" 
                         style="display:flex;align-items:center;gap:8px;">
                        <span id="status_icon_{field_id}" 
                              style="font-size:1.25rem;">
                            {('🟢' if is_live else '⚫')}
                        </span>
                        <span id="status_text_{field_id}"
                              style="font-weight:600;font-size:1rem;
                                     color:{('#22c55e' if is_live else '#6b7280')};">
                            {('LIVE' if is_live else 'DRAFT')}
                        </span>
                    </div>
                </div>
                
                <!-- Status description -->
                <p id="status_desc_{field_id}" 
                   style="color:#9ca3af;font-size:0.875rem;margin-top:8px;margin-bottom:0;">
                    {('Project is visible on the public portfolio.' 
                      if is_live 
                      else 'Project is hidden from the public portfolio.')}
                </p>
            </div>
            
            <script>
                function toggleStatus_{field_id}() {{
                    const input = document.getElementById('{field_id}');
                    const container = document.querySelector('#status_toggle_{field_id} .toggle-container');
                    const knob = document.getElementById('toggle_knob_{field_id}');
                    const icon = document.getElementById('status_icon_{field_id}');
                    const text = document.getElementById('status_text_{field_id}');
                    const desc = document.getElementById('status_desc_{field_id}');
                    
                    const isCurrentlyLive = input.value === 'live';
                    const newStatus = isCurrentlyLive ? 'draft' : 'live';
                    
                    // Update hidden input
                    input.value = newStatus;
                    
                    // Animate toggle
                    if (newStatus === 'live') {{
                        container.style.background = '#22c55e';
                        knob.style.left = '31px';
                        icon.textContent = '🟢';
                        text.textContent = 'LIVE';
                        text.style.color = '#22c55e';
                        desc.textContent = 'Project is visible on the public portfolio.';
                    }} else {{
                        container.style.background = '#374151';
                        knob.style.left = '3px';
                        icon.textContent = '⚫';
                        text.textContent = 'DRAFT';
                        text.style.color = '#6b7280';
                        desc.textContent = 'Project is hidden from the public portfolio.';
                    }}
                }}
            </script>
        ''')



class ZipUploadWidget(TextInput):
    """
    Custom widget for uploading and extracting ZIP archives.
    
    Features:
    - Drag-and-drop zone for ZIP files
    - Progress indicator during upload
    - Integration with ZipExtractService
    - Display of extracted files
    
    Requirements: 2.2, 6.1
    """
    
    def __call__(self, field, **kwargs):
        field_id = field.id
        field_name = field.name
        current_value = field.data or ''
        
        # Show existing path if available
        path_display = ''
        if current_value:
            path_display = f'''
                <div id="current_path_{field_id}" 
                     style="margin-top:10px;padding:10px;background:#1f2937;
                            border-radius:6px;border:1px solid #374151;">
                    <div style="display:flex;align-items:center;gap:8px;">
                        <i class="fa-solid fa-folder-open" style="color:#6366f1;"></i>
                        <span style="color:#e5e7eb;">Current path:</span>
                        <code style="color:#22c55e;">{current_value}</code>
                    </div>
                </div>
            '''
        
        return Markup(f'''
            <div class="zip-upload-widget" id="zip_upload_container">
                <!-- Hidden input for form submission -->
                <input type="hidden" name="{field_name}" id="{field_id}" value="{current_value}">
                
                <!-- Drag-drop zone -->
                <div id="dropzone_{field_id}"
                     ondragover="handleDragOver_{field_id}(event)"
                     ondragleave="handleDragLeave_{field_id}(event)"
                     ondrop="handleDrop_{field_id}(event)"
                     onclick="document.getElementById('file_input_{field_id}').click()"
                     style="border:2px dashed #374151;border-radius:12px;
                            padding:40px 20px;text-align:center;
                            cursor:pointer;transition:all 0.3s ease;
                            background:#111827;">
                    <input type="file" id="file_input_{field_id}" 
                           accept=".zip" style="display:none;"
                           onchange="handleFileSelect_{field_id}(this)">
                    
                    <div id="dropzone_content_{field_id}">
                        <i class="fa-solid fa-file-zipper" 
                           style="font-size:3rem;color:#6366f1;margin-bottom:15px;"></i>
                        <p style="color:#e5e7eb;font-size:1rem;margin:0 0 8px 0;">
                            Drag & drop ZIP file here
                        </p>
                        <p style="color:#6b7280;font-size:0.875rem;margin:0;">
                            or click to browse
                        </p>
                    </div>
                </div>
                
                <!-- Progress bar -->
                <div id="progress_container_{field_id}" style="display:none;margin-top:15px;">
                    <div style="display:flex;justify-content:space-between;margin-bottom:5px;">
                        <span id="progress_text_{field_id}" style="color:#9ca3af;font-size:0.875rem;">
                            Uploading...
                        </span>
                        <span id="progress_percent_{field_id}" style="color:#6366f1;font-size:0.875rem;">
                            0%
                        </span>
                    </div>
                    <div style="background:#1f2937;border-radius:4px;overflow:hidden;height:8px;">
                        <div id="progress_bar_{field_id}" 
                             style="background:linear-gradient(90deg,#6366f1,#a855f7);
                                    height:100%;width:0%;transition:width 0.3s ease;"></div>
                    </div>
                </div>
                
                <!-- Current path display -->
                {path_display}
                
                <!-- Extracted files list -->
                <div id="files_list_{field_id}" style="display:none;margin-top:15px;">
                    <div style="display:flex;align-items:center;gap:8px;margin-bottom:10px;">
                        <i class="fa-solid fa-check-circle" style="color:#22c55e;"></i>
                        <span style="color:#e5e7eb;font-weight:500;">Extracted files:</span>
                    </div>
                    <div id="files_content_{field_id}" 
                         style="background:#1f2937;border-radius:6px;padding:10px;
                                max-height:200px;overflow-y:auto;font-family:monospace;
                                font-size:0.875rem;color:#9ca3af;"></div>
                </div>
                
                <!-- Error display -->
                <div id="error_{field_id}" style="display:none;margin-top:15px;
                     padding:10px;background:#7f1d1d;border-radius:6px;
                     border:1px solid #dc2626;">
                    <div style="display:flex;align-items:center;gap:8px;">
                        <i class="fa-solid fa-exclamation-circle" style="color:#ef4444;"></i>
                        <span id="error_text_{field_id}" style="color:#fca5a5;"></span>
                    </div>
                </div>
            </div>
            
            <script>
                function handleDragOver_{field_id}(event) {{
                    event.preventDefault();
                    event.stopPropagation();
                    const dropzone = document.getElementById('dropzone_{field_id}');
                    dropzone.style.borderColor = '#6366f1';
                    dropzone.style.background = '#1e1b4b';
                }}
                
                function handleDragLeave_{field_id}(event) {{
                    event.preventDefault();
                    event.stopPropagation();
                    const dropzone = document.getElementById('dropzone_{field_id}');
                    dropzone.style.borderColor = '#374151';
                    dropzone.style.background = '#111827';
                }}
                
                function handleDrop_{field_id}(event) {{
                    event.preventDefault();
                    event.stopPropagation();
                    handleDragLeave_{field_id}(event);
                    
                    const files = event.dataTransfer.files;
                    if (files.length > 0) {{
                        processFile_{field_id}(files[0]);
                    }}
                }}
                
                function handleFileSelect_{field_id}(input) {{
                    if (input.files && input.files[0]) {{
                        processFile_{field_id}(input.files[0]);
                    }}
                }}
                
                async function processFile_{field_id}(file) {{
                    // Validate file type
                    if (!file.name.toLowerCase().endsWith('.zip')) {{
                        showError_{field_id}('Please select a ZIP file');
                        return;
                    }}
                    
                    // Validate file size (50MB max)
                    if (file.size > 50 * 1024 * 1024) {{
                        showError_{field_id}('File too large (max 50MB)');
                        return;
                    }}
                    
                    // Get project slug from form
                    const slugInput = document.querySelector('[name="slug"]');
                    if (!slugInput || !slugInput.value) {{
                        showError_{field_id}('Please enter a project slug first');
                        return;
                    }}
                    const slug = slugInput.value;
                    
                    // Show progress
                    hideError_{field_id}();
                    showProgress_{field_id}();
                    
                    // Create form data
                    const formData = new FormData();
                    formData.append('file', file);
                    formData.append('slug', slug);
                    
                    try {{
                        // Upload and extract
                        const response = await fetch('/admin/api/upload-zip', {{
                            method: 'POST',
                            body: formData
                        }});
                        
                        if (!response.ok) {{
                            const error = await response.json();
                            throw new Error(error.detail || 'Upload failed');
                        }}
                        
                        const result = await response.json();
                        
                        // Update hidden input with path
                        document.getElementById('{field_id}').value = result.path;
                        
                        // Show success
                        updateProgress_{field_id}(100, 'Extraction complete!');
                        
                        // Show extracted files
                        if (result.files && result.files.length > 0) {{
                            showFiles_{field_id}(result.files);
                        }}
                        
                        // Update current path display
                        updateCurrentPath_{field_id}(result.path);
                        
                    }} catch (error) {{
                        hideProgress_{field_id}();
                        showError_{field_id}(error.message);
                    }}
                }}
                
                function showProgress_{field_id}() {{
                    document.getElementById('progress_container_{field_id}').style.display = 'block';
                    updateProgress_{field_id}(30, 'Uploading...');
                    
                    // Simulate progress
                    setTimeout(() => updateProgress_{field_id}(60, 'Extracting...'), 500);
                    setTimeout(() => updateProgress_{field_id}(90, 'Validating...'), 1000);
                }}
                
                function hideProgress_{field_id}() {{
                    document.getElementById('progress_container_{field_id}').style.display = 'none';
                }}
                
                function updateProgress_{field_id}(percent, text) {{
                    document.getElementById('progress_bar_{field_id}').style.width = percent + '%';
                    document.getElementById('progress_percent_{field_id}').textContent = percent + '%';
                    document.getElementById('progress_text_{field_id}').textContent = text;
                }}
                
                function showError_{field_id}(message) {{
                    const errorDiv = document.getElementById('error_{field_id}');
                    document.getElementById('error_text_{field_id}').textContent = message;
                    errorDiv.style.display = 'block';
                }}
                
                function hideError_{field_id}() {{
                    document.getElementById('error_{field_id}').style.display = 'none';
                }}
                
                function showFiles_{field_id}(files) {{
                    const container = document.getElementById('files_list_{field_id}');
                    const content = document.getElementById('files_content_{field_id}');
                    
                    content.innerHTML = files.map(f => 
                        '<div style="padding:2px 0;">📄 ' + f + '</div>'
                    ).join('');
                    
                    container.style.display = 'block';
                }}
                
                function updateCurrentPath_{field_id}(path) {{
                    let pathDiv = document.getElementById('current_path_{field_id}');
                    if (!pathDiv) {{
                        pathDiv = document.createElement('div');
                        pathDiv.id = 'current_path_{field_id}';
                        pathDiv.style.cssText = 'margin-top:10px;padding:10px;background:#1f2937;border-radius:6px;border:1px solid #374151;';
                        document.getElementById('zip_upload_container').appendChild(pathDiv);
                    }}
                    pathDiv.innerHTML = `
                        <div style="display:flex;align-items:center;gap:8px;">
                            <i class="fa-solid fa-folder-open" style="color:#6366f1;"></i>
                            <span style="color:#e5e7eb;">Current path:</span>
                            <code style="color:#22c55e;">${{path}}</code>
                        </div>
                    `;
                }}
            </script>
        ''')
