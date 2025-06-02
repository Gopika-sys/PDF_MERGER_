import os
import tempfile
from django.shortcuts import render
from django.http import FileResponse, HttpResponse
from PyPDF4 import PdfFileMerger, PdfFileReader
import io


def index(request):
    """Render the main PDF merger page."""
    return render(request, 'pdf_merger_app/index.html')


def merge_pdfs(request):
    """Process the uploaded PDF files and merge them."""
    if request.method == 'POST' and request.FILES.getlist('pdf_files'):
        # Get the uploaded files
        pdf_files = request.FILES.getlist('pdf_files')
        
        # Create a PDF merger object
        merger = PdfFileMerger()
        
        # Temporary files to store uploaded PDFs
        temp_files = []
        output_path = None
        
        try:
            # Append each PDF to the merger
            for pdf in pdf_files:
                try:
                    # Create a temporary file
                    temp = tempfile.NamedTemporaryFile(delete=False)
                    temp_files.append(temp.name)
                    
                    # Write the uploaded file to the temporary file
                    for chunk in pdf.chunks():
                        temp.write(chunk)
                    temp.close()
                    
                    # First validate the PDF by trying to read it
                    with open(temp.name, 'rb') as pdf_file:
                        # Use strict=False to be more lenient with PDF parsing
                        reader = PdfFileReader(pdf_file, strict=False)
                        # This will throw an exception if the PDF is invalid
                        num_pages = reader.getNumPages()
                    
                    # If we get here, the PDF is valid enough to append
                    merger.append(temp.name)
                    
                except Exception as pdf_error:
                    # Handle individual PDF errors
                    raise Exception(f"Error processing PDF '{pdf.name}': {str(pdf_error)}")
            
            # Create a temporary file for the merged output
            output_file = tempfile.NamedTemporaryFile(delete=False, suffix='.pdf')
            output_path = output_file.name
            output_file.close()
            
            # Write the merged PDF to the file
            with open(output_path, 'wb') as output:
                merger.write(output)
            
            # Close the merger to release file handles
            merger.close()
            
            # Create a response with the file
            response = FileResponse(open(output_path, 'rb'), content_type='application/pdf')
            response['Content-Disposition'] = 'attachment; filename="merged_output.pdf"'
            
            # Let Django handle the file cleanup by registering a callback
            def cleanup_files(files_list, output):
                def cleanup():
                    # Get the underlying file object
                    file_obj = response.file_to_stream
                    if hasattr(file_obj, 'close') and callable(file_obj.close):
                        file_obj.close()
                    
                    # Clean up the temporary files
                    for f in files_list:
                        try:
                            if os.path.exists(f):
                                os.unlink(f)
                        except OSError:
                            pass  # Ignore errors on cleanup
                    
                    # Clean up the output file
                    try:
                        if os.path.exists(output):
                            os.unlink(output)
                    except OSError:
                        pass  # Ignore errors on cleanup
                
                return cleanup
            
            # Store the original close method
            original_close = response.close
            
            # Define a new close method that calls our cleanup function
            def new_close():
                if hasattr(original_close, '__call__'):
                    original_close()
                cleanup_files(temp_files, output_path)()
            
            # Replace the close method
            response.close = new_close
            
            return response
        
        except Exception as e:
            # Ensure merger is closed in case of exception
            try:
                merger.close()
            except:
                pass
            
            # Clean up temporary files if possible
            for temp_file in temp_files:
                try:
                    if os.path.exists(temp_file):
                        os.unlink(temp_file)
                except OSError:
                    pass  # Ignore errors on cleanup
            
            # Clean up output file if created
            if output_path and os.path.exists(output_path):
                try:
                    os.unlink(output_path)
                except OSError:
                    pass  # Ignore errors on cleanup
            
            context = {
                'error_message': f'An error occurred: {str(e)}'
            }
            return render(request, 'pdf_merger_app/index.html', context)
    
    return HttpResponse('No files were uploaded.')
